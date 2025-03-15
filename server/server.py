import socket
from _thread import *
import pickle
import time

from shengJi import ShengJi
from player import Player
from packet import Packet
from simpleGame import SimpleGame

# Global list to keep track of connected clients
numClients = 0
globalGameID = 0
privateGames = {} #a dictionary to store the globalGameID as the key and the game as the value
randomGames = []

dataSize = 1024 * 4

# Set the host to listen on all network interfaces
host = 'localhost'
# Define the port (ensure this port is open on your AWS instance)
port = 12345

# Create a TCP/IP socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((host, port))

#Non client-handling methods
def sendMessage(packet, clientSocket):
    """
    Sends a message to a specified address
    :param packet: The message sent in Packet object form
    :param clientSocket: The destination (client's Socket)
    """
    clientSocket.sendall(pickle.dumps(packet))

def receiveMessage(clientSocket):
    """
    :return: The packet object sent by the client. If no message is received then returns None and closes the client socket
    """
    global numClients
    data = clientSocket.recv(dataSize)
    if not data:
        numClients -= 1
        clientSocket.close()
        return None
    return pickle.loads(data)

def getAllPrivateGamesAsSimplifiedGames() -> list:
    listOfGames = []
    for privateGame in privateGames.values():
        simplifiedGame = SimpleGame(privateGame.getName(), privateGame.getNumPlayersJoined(), privateGame.getID())
        listOfGames.append(simplifiedGame)
    return listOfGames

def getNewGameID() -> int:
    global globalGameID
    """
    Creates a new game ID 
    :return: the game ID generated as an integer
    """
    globalGameID += 1
    return globalGameID

def addNewPrivateGame(gameID: int, privateGame):
    """
    Adds a new game to the global private games list
    """
    global privateGames
    privateGames[gameID] = privateGame

def getPrivateGame(gameID: int):
    """
    Gets a game with the gameID from the global private games list. If not found, returns None
    """
    global privateGames
    if gameID not in privateGames.keys():
        return None
    return privateGames[gameID]

def removePrivateGame(gameID: int):
    """
    Removes a private game
    """
    global privateGames
    del(privateGames[gameID])

def cleanPrivateGames():
    """
    Removes empty private games
    """
    global privateGames
    for game in privateGames.values():
        gameID = game.getID()
        if game.getNumPlayersJoined() == 0:
            removePrivateGame(gameID)

def cleanRandomGames():
    """
    Removes empty randomly joined games
    """
    global randomGames
    for game in randomGames:
        if game.getNumPlayersJoined() == 0:
            removeRandomGame(game)

def removeRandomGame(game):
    """
    Removes a game created through random game joining
    """
    global randomGames
    del(randomGames[randomGames.index(game)])

def wrongPacketMessageReceived(player):
    """
    Action to take if the player object passed doesn't return the expected packet
    """
    global numClients
    numClients -= 1
    player.getSocket().close()

def dealCards(game):
    """
    Deals the cards slowly to the players
    :returns: The eight cards left at the bottom of the deck
    """
    players = game.getPlayers()
    game.makeDeck() #2 decks with jokers, 108 cards
    deck = game.getDeck()
    #leaves the bottom 8 cards
    for _ in range(25):
        for player in players:
            card = deck.drawCard()
            player.addCardToHand(card)
            message = Packet("addCardToHand", card)
            sendMessage(message, player.getSocket())
            packet = receiveMessage(player.getSocket())
            if not packet.getAction() == card and not packet.getValue() == "addedCardToHand":
                wrongPacketMessageReceived(player)

            time.sleep(0.25)

    return deck

def setTrumpSuitDuringDealing(player, game):
    clientSocket = player.getSocket()
    players = game.getPlayers()
    level = game.getLevel()
    trumpSuit = game.getTrumpSuit()
    #checking for initial setting
    while trumpSuit is None:
        packet = receiveMessage(clientSocket)
        if packet.getAction() == "setTrumpSuit":
            value, suit = packet.getValue()
            if value == level:
                trumpSuit = suit
                game.setTrumpSuit(trumpSuit)
                for player in players:
                    connection = player.getSocket()
                    message = Packet("changedTrumpSuit", packet.getValue())
            else:
                message = Packet("invalidCard", "")
                sendMessage(message, clientSocket)

def gameLoopForEachClient(player, game):
    """
    The general game loop
    :param player: The player object of the client
    :param game: The game object the client is connected to
    """
    #deal the cards
    if game.getPlayerIndex(player) == 0:
        start_new_thread(dealCards, (game,))
    #does this have to be a threaded method?
    start_new_thread(setTrumpSuitDuringDealing, (player, game)):



def startPrivateGame(player, gameID: int):
    """
    Starts a game with the specified gameID
    """
    global privateGames
    game = privateGames[gameID]
    gameLoopForEachClient(player, game)

def startRandomGame(player, gameIndex: int):
    """
    Starts a game with the specified index
    """
    global randomGames
    game = randomGames[gameIndex]
    gameLoopForEachClient(player, game)

def gameCleaner():
    while True:
        if not numClients == 0:
            cleanRandomGames()
            cleanPrivateGames()
            time.sleep(600)
        else:
            time.sleep(3600)

#threaded client handling methods
def joinRandomGame(player):
    global randomGames
    clientSocket = player.getSocket()
    mostRecentlyCreatedGame = randomGames[-1]
    gameIndex = randomGames.index(mostRecentlyCreatedGame)
    if mostRecentlyCreatedGame.getNumPlayersJoined() == 4: #game is full
        gameID = getNewGameID()
        newRandomGame = ShengJi(gameID)
        randomGames.append(newRandomGame)
        newRandomGame.addNewPlayer(player)
        message = Packet("joinedRandomGame", gameID)
    else: #game isn't full
        mostRecentlyCreatedGame.addNewPlayer(player)
        message = Packet("joinedRandomGame", mostRecentlyCreatedGame.getID())
    sendMessage(message, clientSocket)

    while not mostRecentlyCreatedGame.getNumPlayersJoined() == 4:
        numPlayers = mostRecentlyCreatedGame.getNumPlayersJoined()
        message = Packet("numberOfPlayersInGame", numPlayers)
        sendMessage(message, clientSocket)

        packet = receiveMessage(clientSocket)
        if not packet.getAction() == "gotTotalPlayers" and not packet.getValue() == numPlayers:
            wrongPacketMessageReceived(player)

    message = Packet("startingGame", "")
    sendMessage(message, clientSocket)
    packet = receiveMessage(clientSocket)
    if not packet.getAction() == "readyToPlay":
        wrongPacketMessageReceived(player)

    startRandomGame(player, gameIndex)

def joinPrivateGame(player, gameID: int):
    global privateGames
    clientSocket = player.getSocket()
    if gameID not in privateGames.keys():
        message = Packet("failedToJoinPrivateGame", "Private game not found.")
    elif privateGames[gameID].getNumPlayersJoined() == 4:
        message = Packet("failedToJoinPrivateGame", "Private game full.")
    else:
        message = Packet("joinedPrivateGame", gameID)
    sendMessage(message, clientSocket)

    game = privateGames[gameID]
    while not game.getNumPlayersJoined() == 4:
        continue

    message = Packet("startingGame", "")
    sendMessage(message, clientSocket)
    packet = receiveMessage(clientSocket)
    if not packet.getAction() == "readyToPlay":
        wrongPacketMessageReceived(player)

    startPrivateGame(player, gameID)
    """while True:
        if game.allReady():
            startPrivateGame(gameID)
            return
        else:
            #can add implementation of showing other player's ready state later
            continue"""

def createPrivateGame(player, gameName):
    gameID = getNewGameID() #generate a new gameID
    privateGame = ShengJi(gameID)
    addNewPrivateGame(gameID, privateGame)
    privateGame.addNewPlayer(player)
    privateGame.setName(gameName)

    message = Packet("createdNewPrivateGame", gameName)
    sendMessage(message, player)

    clientSocket = player.getSocket()
    while True:
        ready = privateGame.allReady()
        if ready:
            break
        else:
            numPlayers = 0
            #sends an update when the number of players in the game changes
            if not numPlayers == privateGame.getNumPlayersJoined():
                numPlayers = privateGame.getNumPlayersJoined()
                message = Packet("setTotalPlayers", numPlayers)
                sendMessage(message, clientSocket)
                packet = receiveMessage(clientSocket)
                if not packet.getAction() == "gotTotalPlayers" or not packet.getValue() == numPlayers:
                    wrongPacketMessageReceived(player)

    startPrivateGame(player, gameID)

def privateLobbyWaiting(player):
    """
    Actions for the client while they are watching the private lobby screen
    :param player: Player object of the client
    """
    clientSocket = player.getSocket()
    run = True
    while run:
        packet = receiveMessage(clientSocket)
        action = packet.getAction()
        if action == "getPrivateGames":
            listOfGames = getAllPrivateGamesAsSimplifiedGames()
            message = Packet("returnPrivateGames", listOfGames)
            sendMessage(message, clientSocket)
        else:
            run = False
            exit_thread()
            if action == "joinRandomGame":
                start_new_thread(joinRandomGame, (player,))
            elif action == "setPrivateGameName":
                gameName = packet.getValue()
                start_new_thread(createPrivateGame, (player, gameName))
            elif action == "joinPrivateGame":
                gameID = packet.getValue()
                start_new_thread(joinPrivateGame, (player, gameID))


def main():
    global numClients
    serverSocket.listen()  # Start listening for incoming connections
    print(f"Server listening on {host}:{port}")

    start_new_thread(gameCleaner, ())

    while True:
        clientSocket, clientAddress = serverSocket.accept()
        numClients += 1
        player = Player()
        player.setSocket(clientSocket)
        print("Connected to:", clientAddress)
        message = Packet("setDataSize", dataSize)
        sendMessage(message, clientSocket)
        packet = receiveMessage(clientSocket)
        if not packet.getAction() == "gotDataSize" or not packet.getValue() == dataSize:
            wrongPacketMessageReceived(player)

        #Client first sends their name
        packet = receiveMessage(clientSocket)
        if packet.getAction() == "setPlayerName":
            player.setName(packet.getValue())
            message = Packet("gotPlayerName", packet.getValue())
            sendMessage(message, clientSocket)

        #Client then sends if they are getting private privateGames, joining a random game, or creating a new private game
        packet = receiveMessage(clientSocket)
        if packet.getAction() == "getPrivateGames":
            listOfGames = getAllPrivateGamesAsSimplifiedGames()
            message = Packet("returnPrivateGames", listOfGames)
            sendMessage(message, clientSocket)
            start_new_thread(privateLobbyWaiting, (player,))

        elif packet.getAction() == "joinRandomGame":
            start_new_thread(joinRandomGame, (player,))

        elif packet.getAction() == "setPrivateGameName":
            gameName = packet.getValue()
            message = Packet("createNewPrivateGame", gameName)
            sendMessage(message, clientSocket)
            start_new_thread(joinPrivateGame, (player, gameName))
        #can't join the private games if the client hasn't received the games yet

#running server
main()
import socket
from _thread import *
import pickle
import time

from shengJi import ShengJi
from player import Player
from packet import Packet
from simpleGame import SimpleGame
from card_logic import Card

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

# Create a TCP/IP playerSocket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((host, port))

#Non client-handling methods
def sendMessage(packet: Packet, clientSocket: socket) -> None:
    """
    Sends a message to a specified address
    :param packet: The message sent in Packet object form
    :param clientSocket: The destination (client's Socket)
    """
    clientSocket.sendall(pickle.dumps(packet))

def receiveMessage(clientSocket: socket) -> Packet | None:
    """
    :return: The packet object sent by the client. If no message is received then returns None and closes the client playerSocket
    """
    global numClients
    message = clientSocket.recv(dataSize)
    if not message:
        numClients -= 1
        clientSocket.close()
        return None
    message = pickle.loads(message)
    print(f"Received {message} from {clientSocket}")
    return message

def sendMessageToAllInGame(message: Packet, game: ShengJi):
    players = game.getPlayers()
    for player in players:
        sendMessage(message, player.getSocket())

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

def addNewPrivateGame(gameID: int, privateGame: ShengJi):
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

def removePrivateGame(game: ShengJi):
    """
    Removes a private game
    """
    global privateGames
    del privateGames[game.getID()]

def cleanPrivateGames():
    """
    Removes empty private games
    """
    global privateGames
    for game in privateGames.values():
        if game.getNumPlayersJoined() == 0:
            removePrivateGame(game)

def cleanRandomGames():
    """
    Removes empty randomly joined games
    """
    global randomGames
    for game in randomGames:
        if game.getNumPlayersJoined() == 0:
            removeRandomGame(game)

def removeRandomGame(game: ShengJi):
    """
    Removes a game created through random game joining
    """
    global randomGames
    del randomGames[randomGames.index(game)]

def wrongPacketMessageReceived(player: Player):
    """
    Action to take if the player object passed doesn't return the expected packet
    """
    global numClients
    numClients -= 1
    player.getSocket().close()
    del player

def dealCards(game: ShengJi):
    """
    Deals the cards slowly to the players
    :returns: The eight cards left at the bottom of the deck
    """
    players = game.getPlayers()
    deck = game.getDeck()
    deck.shuffleDeck()
    #leaves the bottom 8 cards
    for _ in range(25):
        for player in players:
            card = deck.drawCard()
            player.addCardToHand(card)
            message = Packet("add card to hand", card)
            sendMessage(message, player.getSocket())
            packet = receiveMessage(player.getSocket())
            if not packet.getValue() == card and not packet.getAction() == "added card to hand":
                wrongPacketMessageReceived(player)

            time.sleep(0.25)

    return deck

def gameLoopForEachClient(player: Player, game: ShengJi):
    """
    The general game loop
    :param player: The player object of the client
    :param game: The game object the client is connected to
    """
    clientSocket = player.getSocket()
    playerIndex = game.getPlayerIndex(player)
    level = game.getLevel()
    trumpSuit = game.getTrumpSuit()
    #deal the cards
    if game.getPlayerIndex(player) == 0:
        start_new_thread(dealCards, (game,))
    readyToPlay = game.allReady()
    reinforcedTrumpSuit = False
    while not readyToPlay and not trumpSuit:
        packet = receiveMessage(clientSocket)
        if packet.getAction() == "ready to play":
            game.setPlayerReady(player, True)
            message = Packet("got ready to play")
            sendMessage(message, clientSocket)

        elif packet.getAction() == "set trump suit":
            simpleCards = packet.getValue()  # array of value, suit pairs

            if len(simpleCards) == 2:
                value, suit = simpleCards
                if trumpSuit:
                    if playerIndex == game.getTrickStarter() and suit == game.getTrumpSuit() and value == game.getLevel():
                        reinforcedTrumpSuit = True
                        message = Packet("reinforced trump suit", suit)
                        sendMessageToAllInGame(message, game)
                else:
                    if suit == game.getTrumpSuit() and value == game.getLevel():
                        message = Packet("set trump suit", suit)
                        sendMessageToAllInGame(message, game)
                    else:
                        message = Packet("invalid card")
                        sendMessage(message, clientSocket)

            elif simpleCards[0] == simpleCards[2] and simpleCards[1] == simpleCards[3]:
                if not reinforcedTrumpSuit:
                    trumpSuit = None
                    if simpleCards[1] == "joker":
                        game.setColorOfTrumpSuitIfJoker(simpleCards[0])
                        trumpSuit = simpleCards[1]
                    elif simpleCards[0] == game.getLevel():
                        trumpSuit = simpleCards[1]

                    if trumpSuit:
                        reinforcedTrumpSuit = True
                        game.setTrumpSuit(trumpSuit)
                        game.setTrickStarter(playerIndex)
                        message = Packet("reinforced trump suit", [simpleCards[0], simpleCards[1]])
                        sendMessageToAllInGame(message, game)
                    else:
                        message = Packet("invalid card")
                        sendMessage(message, clientSocket)

                #reinforced trump suit
                else:
                    jokerColor = game.getColorOfTrumpSuitIfJoker()
                    newCard = Card(simpleCards[0], simpleCards[1], -1, "")
                    if jokerColor:
                        oldCard = Card(jokerColor, "joker", -1, "")
                    else:
                        oldCard = Card(game.getLevel(), game.getTrumpSuit(), -1, "")

                    if newCard > oldCard:
                        game.setTrumpSuit(simpleCards[1])
                        game.setTrickStarter(playerIndex)
                        message = Packet("changed trump suit", [simpleCards[0], simpleCards[1]])
                        if simpleCards[1] == "joker":
                            game.setColorOfTrumpSuitIfJoker(simpleCards[0])

                        sendMessageToAllInGame(message, game)
                    else:
                        message = Packet("invalid card")
                        sendMessage(message, clientSocket)
            else:
                message = Packet("invalid card")
                sendMessage(message, clientSocket)
        trumpSuit = game.getTrumpSuit()

    #actual gameplay
    while player.getHand():
        if playerIndex == game.getTrickStarter():
            packet = receiveMessage(clientSocket)
            if packet.getAction() == "play cards":
                cards = packet.getValue()
                if len(cards) == 1:
                    cards = cards[0]
                    card = Card(cards.getValue(), cards.getSuit(), )
                if len(cards) == 2 and cards[0] == cards[1]:
                    c0, c1 = cards
                    card1 = Card(c0.getValue(), c0.getSuit())
                    game.playCard()



def startPrivateGame(player: Player, gameID: int):
    """
    Starts a game with the specified gameID
    """
    global privateGames
    game = privateGames[gameID]
    gameLoopForEachClient(player, game)

def startRandomGame(player: Player, gameIndex: int):
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

def updatePlayerCountLoop(player: Player, game: ShengJi):
    clientSocket = player.getSocket()
    while not game.allReady():
        numPlayers = 0
        # sends an update when the number of players in the game changes
        if not numPlayers == game.getNumPlayersJoined():
            numPlayers = game.getNumPlayersJoined()
            message = Packet("set total players", numPlayers)
            sendMessage(message, clientSocket)
            packet = receiveMessage(clientSocket)
            if not packet.getAction() == "got total players" or not packet.getValue() == numPlayers:
                wrongPacketMessageReceived(player)


#threaded client handling methods
def joinRandomGame(player: Player):
    global randomGames
    clientSocket = player.getSocket()
    mostRecentlyCreatedGame = randomGames[-1]
    gameIndex = randomGames.index(mostRecentlyCreatedGame)
    if mostRecentlyCreatedGame.getNumPlayersJoined() == 4: #game is full
        gameID = getNewGameID()
        mostRecentlyCreatedGame = ShengJi(gameID)
        randomGames.append(mostRecentlyCreatedGame)
        mostRecentlyCreatedGame.addNewPlayer(player)
        player.setGame(mostRecentlyCreatedGame)
        message = Packet("joinedRandomGame", gameID)
    else: #game isn't full
        mostRecentlyCreatedGame.addNewPlayer(player)
        player.setGame(mostRecentlyCreatedGame)
        message = Packet("joinedRandomGame", mostRecentlyCreatedGame.getID())
    sendMessage(message, clientSocket)

    updatePlayerCountLoop(player, mostRecentlyCreatedGame)

    message = Packet("starting game")
    sendMessage(message, clientSocket)
    packet = receiveMessage(clientSocket)
    if not packet.getAction() == "ready to play":
        wrongPacketMessageReceived(player)

    startRandomGame(player, gameIndex)

def joinPrivateGame(player: Player, gameID: int):
    global privateGames
    clientSocket = player.getSocket()
    if gameID not in privateGames.keys():
        message = Packet("failed to join private game", "Private game not found.")
    elif privateGames[gameID].getNumPlayersJoined() == 4:
        message = Packet("failed to join private game", "Private game full.")
    else:
        message = Packet("joined private game", gameID)
    sendMessage(message, clientSocket)

    game = privateGames[gameID]
    updatePlayerCountLoop(player, game)

    message = Packet("starting game")
    sendMessage(message, clientSocket)
    packet = receiveMessage(clientSocket)
    if not packet.getAction() == "ready to play":
        wrongPacketMessageReceived(player)

    startPrivateGame(player, gameID)
    """while True:
        if game.allReady():
            startPrivateGame(gameID)
            return
        else:
            #can add implementation of showing other player's ready state later
            continue"""

def createPrivateGame(player: Player, gameName: str):
    gameID = getNewGameID() #generate a new gameID
    privateGame = ShengJi(gameID)
    addNewPrivateGame(gameID, privateGame)
    privateGame.addNewPlayer(player)
    privateGame.setName(gameName)
    player.setGame(privateGame)

    message = Packet("created new private game", gameName)
    sendMessage(message, player)

    updatePlayerCountLoop(player, privateGame)

    startPrivateGame(player, gameID)

def waitingInPrivateLobby(player: Player):
    """
    Actions for the client while they are watching the private lobby screen
    :param player: Player object of the client
    """
    clientSocket = player.getSocket()
    while True:
        packet = receiveMessage(clientSocket)
        action = packet.getAction()
        if action == "get private games":
            listOfGames = getAllPrivateGamesAsSimplifiedGames()
            message = Packet("return private games", listOfGames)
            sendMessage(message, clientSocket)
        else:
            if action == "join random game":
                joinRandomGame(player)
            elif action == "create private game":
                gameName = packet.getValue()
                createPrivateGame(player, gameName)
            elif action == "join private game":
                gameID = packet.getValue()
                joinPrivateGame(player, gameID)
            break


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
        message = Packet("set data size", dataSize)
        sendMessage(message, clientSocket)
        packet = receiveMessage(clientSocket)
        if not packet.getAction() == "got data size" or not packet.getValue() == dataSize:
            wrongPacketMessageReceived(player)

        #Client first sends their name
        packet = receiveMessage(clientSocket)
        if packet.getAction() == "set player name":
            player.setName(packet.getValue())
            message = Packet("got player name", packet.getValue())
            sendMessage(message, clientSocket)

        #Client then sends if they are getting private privateGames, joining a random game, or creating a new private game
        packet = receiveMessage(clientSocket)
        if packet.getAction() == "get private games":
            listOfGames = getAllPrivateGamesAsSimplifiedGames()
            message = Packet("return private games", listOfGames)
            sendMessage(message, clientSocket)
            start_new_thread(waitingInPrivateLobby, (player,))

        elif packet.getAction() == "join random game":
            start_new_thread(joinRandomGame, (player,))

        elif packet.getAction() == "create private game":
            gameName = packet.getValue()
            message = Packet("createNewPrivateGame", gameName)
            sendMessage(message, clientSocket)
            start_new_thread(joinPrivateGame, (player, gameName))
        else:
            wrongPacketMessageReceived(player)
        #can't join the private games if the client hasn't received the games yet

#running server
main()
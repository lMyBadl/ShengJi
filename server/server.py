import socket
from _thread import *
import pickle

from shengJi import ShengJi
from player import Player
from packet import Packet
from simpleGame import SimpleGame

# Global list to keep track of connected clients
clients = {}
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
def sendMessage(packet: list, clientSocket):
    """
    Sends a message to a specified address
    :param packet: The message sent in Packet object form
    :param clientSocket: The destination (client's Socket)
    """
    clientSocket.sendall(pickle.dumps(packet))

def receiveMessage(clientSocket) -> list:
    """
    :return: A list containing the packet objects sent by the client. If no message is received then returns [] and closes the client socket
    """
    data = clientSocket.recv(dataSize)
    if not data:
        clientSocket.close()
        return []
    return pickle.loads(data)

def getAllPrivateGamesAsSimplifiedGames() -> list:
    listOfGames = []
    for privateGame in privateGames.values():
        simplifiedGame = SimpleGame(privateGame.getName(), privateGame.getPlayersJoined(), privateGame.getID())
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

#threaded client handling methods
def clientHandler(player, playerNum: int, gameID: int, gameType: str):
    """
    Handles communication with a connected client.
    :param player: Player object
    :param playerNum: The player number in the game [0, 1, 2, 3]
    :param gameID: The game ID of the game the player is connected to
    :param gameType: private, waiting, or random
    :return:
    """
    clientSocket = player.getSocket()
    if gameType == "private":

    elif gameType == "random":

    elif gameType == "waiting":

    playerID = player.getID()


    clients[playerID] = clientSocket  # Store the player socket

    message = [Packet("assignId", playerID)]
    sendMessage(message, clientSocket)
    #print(f"New socket from {playerId} at {addr}")

    run = True
    while run:
        try:
            receiveMessage(clientSocket)

        except Exception as e:
            print(f"Error with player {playerID}: {e}")
            break

    # Remove the client from the dictionary upon disconnect
    print(f"Player {playerID} disconnected.")
    del clients[playerID]
    clientSocket.close()

def joinRandomGame(player):


def joinPrivateGame(player, gameID):


def createPrivateGame(player, gameName):
    gameID = getNewGameID() #generate a new gameID
    privateGame = ShengJi(gameID)
    addNewPrivateGame(gameID, privateGame)
    privateGame.addNewPlayer(player)
    privateGame.setName(gameName)

    message = [Packet("createNewPrivateGame", gameName)]
    sendMessage(message, player)

def privateLobbyWaiting(player):
    """
    Actions for the client while they are watching the private lobby screen
    :param player: Player object of the client
    """
    clientSocket = player.getSocket()
    run = True
    while run:
        packets = receiveMessage(clientSocket)
        for packet in packets:
            action = packet.getAction()
            if action == "getPrivateGames":
                listOfGames = getAllPrivateGamesAsSimplifiedGames()
                message = [Packet("returnPrivateGames", listOfGames)]
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
    serverSocket.listen()  # Start listening for incoming connections
    print(f"Server listening on {host}:{port}")

    while True:
        clientSocket, clientAddress = serverSocket.accept()
        player = Player()
        player.setSocket(clientSocket)
        print("Connected to:", clientAddress)
        message = [Packet("setDataSize", dataSize)]
        sendMessage(message, clientSocket)
        packets = receiveMessage(clientSocket)
        for packet in packets:
            if not packet.getAction() == "gotDataSize" or not packet.getValue() == dataSize:
                clientSocket.close()

        #Client first sends their name
        packets = receiveMessage(clientSocket)
        for packet in packets:
            if packet.getAction() == "setPlayerName":
                player.setName(packet.getValue())
                message = [Packet("gotPlayerName", packet.getValue())]
                sendMessage(message, clientSocket)

        #Client then sends if they are getting private privateGames, joining a random game, or creating a new private game
        packets = receiveMessage(clientSocket)
        for packet in packets:
            if packet.getAction() == "getPrivateGames":
                listOfGames = getAllPrivateGamesAsSimplifiedGames()
                message = [Packet("returnPrivateGames", listOfGames)]
                sendMessage(message, clientSocket)
                start_new_thread(privateLobbyWaiting, (player,))

            elif packet.getAction() == "joinRandomGame":
                start_new_thread(joinRandomGame, (player,))

            elif packet.getAction() == "setPrivateGameName":
                gameName = packet.getValue()
                message = [Packet("createNewPrivateGame", gameName)]
                sendMessage(message, clientSocket)
                start_new_thread(joinPrivateGame, (player, gameName))
            #can't join the private games if the client hasn't received the games yet

#running server
main()
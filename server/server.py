import socket
from _thread import *
import pickle

from shengJi import ShengJi
from player import Player
from packet import Packet
from simpleGame import SimpleGame

# Global list to keep track of connected clients
clients = {}
gameId = 0
privateGames = {} #a dictionary to store the gameID as the key and the game as the value
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
    :return: A dictionary containing the action name as the key and the action as the value. If no message is received then returns {None:None}
    """
    data = clientSocket.recv(dataSize)
    if not data:
        return [None]
    return pickle.loads(data)

def getAllPrivateGamesAsSimplifiedGames() -> list:
    listOfGames = []
    for privateGame in privateGames.values():
        simplifiedGame = SimpleGame(privateGame.getName(), privateGame.getPlayersJoined(), privateGame.getID())
        listOfGames.append(simplifiedGame)
    return listOfGames

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

def joinPrivateG

def privateLobbyWaiting(player):
    """
    Actions for the client while they are watching the private lobby screen
    :param player: Player object of the client
    """
    clientSocket = player.getSocket()
    clientName = player.getName()
    run = True
    while run:
        packets = receiveMessage(clientSocket)
        for packet in packets:
            action = packet.getAction()
            if action == "joinRandomGame":
                run = False
            elif action == "setPrivateGameName":
                run = False
            elif action == "getPrivateGames":
                listOfGames = getAllPrivateGamesAsSimplifiedGames()
                message = [Packet("returnPrivateGames", listOfGames)]
                sendMessage(message, clientSocket)
            elif action == "joinPrivateGame":
                pass


def main():
    global gameId
    serverSocket.listen()  # Start listening for incoming connections
    print(f"Server listening on {host}:{port}")

    while True:
        clientSocket, clientAddress = serverSocket.accept()
        player = Player()
        player.setSocket(clientSocket)
        print("Connected to:", clientAddress)
        message = [Packet("setDataSize", dataSize)]
        sendMessage(message, clientSocket)

        #Client first sends their name
        packets = receiveMessage(clientSocket)
        for packet in packets:
            if packet.getAction() == "setPlayerName":
                player.setName(packet.getValue())

        #Client then sends if they are getting private privateGames or joining a random game
        packets = receiveMessage(clientSocket)
        for packet in packets:
            if packet.getAction() == "getPrivateGames":
                listOfGames = getAllPrivateGamesAsSimplifiedGames()
                message = [Packet("returnPrivateGames", listOfGames)]
                sendMessage(message, clientSocket)
                start_new_thread(privateLobbyWaiting, (player,))
            elif packet.getAction() == "joinRandomGame":
                lastRandomGame = randomGames[-1]
                if not lastRandomGame.isFilled():
                    playerNumber = lastRandomGame.addNewPlayer(player)
                    gameId = lastRandomGame.getID()
                    start_new_thread(clientHandler, (player, playerNumber, gameId))
                else:
                    randomGames.append(ShengJi(gameId))
                    lastRandomGame = randomGames[-1]
                    lastRandomGame.addNewPlayer(player)
            elif packet.getAction() == "setPrivateGameName":



        """
        gameID = (idCount - 1) // 4
        p = 0
        if idCount % 4 == 1:
            privateGames[gameID] = ShengJi(gameID, Player(), Player(), Player(), Player())
            privateGames[gameID].getPlayerFromIndex(0).setId(0)
            print("Creating a new game...")
        elif idCount % 4 == 2:
            privateGames[gameID].getPlayerFromIndex(1).setId(1)
            p = 1
        elif idCount % 4 == 3:
            privateGames[gameID].getPlayerFromIndex(2).setId(2)
            p = 2
        elif idCount % 4 == 0:
            privateGames[gameID].getPlayerFromIndex(3).setId(3)
            p = 3
            privateGames[gameID].setReady(True)  # Generate a unique player ID
        """

main()

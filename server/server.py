import socket
from _thread import *
import pickle

from shengJi import ShengJi
from player import Player
from packet import Packet

# Global list to keep track of connected clients
clients = {}
gameId = 0
privateGames = {} #a dictionary to store the game as the key and the simplified game as the value
randomGames = []

dataSize = 1024 * 4

# Set the host to listen on all network interfaces
host = 'localhost'
# Define the port (ensure this port is open on your AWS instance)
port = 12345

# Create a TCP/IP socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((host, port))

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
            data = clientSocket.recv(dataSize)
            if not data: break

            packets = pickle.loads(data)
            for packet in packets:
                action = packet.getAction()
                value = packet.getValue()
                if action == "setGameName":
                    game.setName(value)
            print(f"Received message from {playerID}: {str(packets)}")

        except Exception as e:
            print(f"Error with player {playerID}: {e}")
            break

    # Remove the client from the dictionary upon disconnect
    print(f"Player {playerID} disconnected.")
    del clients[playerID]
    clientSocket.close()

"""
def deal_cards(gameID: int):
    
    num_players = 4
    if num_players == 0:
        return

    cards_per_player = len(deck) // num_players
    print(f"Dealing {cards_per_player} cards to each of {num_players} players.")

    # Store each player's hand
    hands = {}
    for i, playerNumber in enumerate(client_list.keys()):
        hands[playerNumber] = deck[i * cards_per_player:(i + 1) * cards_per_player]

    # Notify each player of their hand and opponent card counts
    for playerNumber, conn in client_list.items():
        opponent_counts = {pid: len(hands[pid]) for pid in hands if pid != playerNumber}
        message = {
            "action": "deal_cards",
            "player_hand": hands[playerNumber],
            "opponent_counts": opponent_counts
        }
        try:
            conn.sendall(json.dumps(message).encode())
            print(f"Sent {len(hands[playerNumber])} cards to player {playerNumber} with opponents: {opponent_counts}")
        except Exception as e:
            print(f"Error sending cards to player {playerNumber}: {e}")"""


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
                listOfGames = []
                for simplifiedGame in privateGames.values():
                    listOfGames.append(simplifiedGame)
                message = [Packet("getPrivateGames", listOfGames)]
                sendMessage(message, clientSocket)
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

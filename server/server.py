import socket
from _thread import *
import pickle

from shengJi import ShengJi
from player import Player
from packet import Packet

# Global list to keep track of connected clients
clients = {}
gameId = 0
idCount = 0
games = {}

dataSize = 1024 * 4

def sendMessage(connection, packet: list):
    """
    Available actions: sendCard, assignPlayerNum, setDataSize
    """
    connection.sendall(pickle.dumps(packet))

def receiveMessage(self) -> list:
    """
    :return: A dictionary containing the action name as the key and the action as the value. If no message is received then returns {None:None}
    """
    data = self.socket.recv(dataSize)
    if not data:
        return None
    return pickle.loads(data)

def clientHandler(client: tuple, playerNum, gameCode):
    """
    Handles communication with a connected client.
    """
    run = gameCode in games
    conn, addr = client

    # gets the pre-generated player id from the game
    game = games[gameCode]
    player = game.getPlayerFromIndex(playerNum)
    player.setSocket(client)
    playerId = player.getId()


    clients[playerId] = conn  # Store the player socket

    message = [Packet("assignId", playerId), Packet("setDataSize", dataSize)]
    sendMessage(conn, message)
    print(f"New socket from {playerId} at {addr}")

    while run:
        try:
            data = conn.recv(dataSize)
            if not data: break

            packets = pickle.loads(data)
            for packet in packets:
                action = packet.getAction()
                value = packet.getValue()
                if action == "setGameName":
                    game.setName(value)
            print(f"Received message from {playerId}: {str(packets)}")

        except Exception as e:
            print(f"Error with player {playerId}: {e}")
            break

    # Remove the client from the dictionary upon disconnect
    print(f"Player {playerId} disconnected.")
    idCount -= 1
    del clients[playerId]
    conn.close()

"""
def deal_cards(gameId: int):
    
    num_players = 4
    if num_players == 0:
        return

    cards_per_player = len(deck) // num_players
    print(f"Dealing {cards_per_player} cards to each of {num_players} players.")

    # Store each player's hand
    hands = {}
    for i, playerId in enumerate(client_list.keys()):
        hands[playerId] = deck[i * cards_per_player:(i + 1) * cards_per_player]

    # Notify each player of their hand and opponent card counts
    for playerId, conn in client_list.items():
        opponent_counts = {pid: len(hands[pid]) for pid in hands if pid != playerId}
        message = {
            "action": "deal_cards",
            "player_hand": hands[playerId],
            "opponent_counts": opponent_counts
        }
        try:
            conn.sendall(json.dumps(message).encode())
            print(f"Sent {len(hands[playerId])} cards to player {playerId} with opponents: {opponent_counts}")
        except Exception as e:
            print(f"Error sending cards to player {playerId}: {e}")"""


def main():
    global idCount, gameId
    # Set the host to listen on all network interfaces
    host = 'localhost'
    # Define the port (ensure this port is open on your AWS instance)
    port = 12345

    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()  # Start listening for incoming connections
    print(f"Server listening on {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        print("Connected to:", addr)

        idCount += 1
        gameId = (idCount - 1) // 4
        p = 0
        if idCount % 4 == 1:
            games[gameId] = ShengJi(gameId, Player(), Player(), Player(), Player())
            games[gameId].getPlayerFromIndex(0).setId(0)
            print("Creating a new game...")
        elif idCount % 4 == 2:
            games[gameId].getPlayerFromIndex(1).setId(1)
            p = 1
        elif idCount % 4 == 3:
            games[gameId].getPlayerFromIndex(2).setId(2)
            p = 2
        elif idCount % 4 == 0:
            games[gameId].getPlayerFromIndex(3).setId(3)
            p = 3
            games[gameId].setReady(True)  # Generate a unique player ID

        start_new_thread(clientHandler, ((conn, addr), p, gameId))

if __name__ == '__main__':
    main()

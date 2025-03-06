# server.py
import socket  # For network connections
import threading  # To handle multiple clients concurrently
import json  # For encoding/decoding messages in JSON
import random  # To shuffle the deck
import uuid #used for generating unique user IDs
# Global list to keep track of connected clients
clients = {}


def client_handler(conn, addr):
    """
    Handles communication with a connected client.
    """
    player_id = str(uuid.uuid4())[:8]  # Generate a unique player ID
    clients[player_id] = conn  # Store the player socket

    welcome_message = {"action": "assign_id", "player_id": player_id}
    conn.sendall(json.dumps(welcome_message).encode())
    print(f"New connection from {player_id} at {addr}")

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break

            message = json.loads(data.decode())
            print(f"Received message from {player_id}: {message}")

            if message.get("action") == "deal_request":
                print(f"Player {player_id} requested cards.")
                deal_cards(clients)  # ✅ Ensure the full `clients` dictionary is passed

        except Exception as e:
            print(f"Error with player {player_id}: {e}")
            break

    # Remove the client from the dictionary upon disconnect
    print(f"Player {player_id} disconnected.")
    del clients[player_id]
    conn.close()



def deal_cards(client_list):
    """
    Deals out all the cards in a standard deck (52 cards) evenly to all connected clients.
    """
    suits = ['Hearts', 'Diamond', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '1']
    deck = [f"{suit} {rank}" for suit in suits for rank in ranks]
    random.shuffle(deck)

    num_players = len(client_list)
    if num_players == 0:
        return

    cards_per_player = len(deck) // num_players
    print(f"Dealing {cards_per_player} cards to each of {num_players} players.")

    # Store each player's hand
    hands = {}
    for i, player_id in enumerate(client_list.keys()):
        hands[player_id] = deck[i * cards_per_player:(i + 1) * cards_per_player]

    # Notify each player of their hand and opponent card counts
    for player_id, conn in client_list.items():
        opponent_counts = {pid: len(hands[pid]) for pid in hands if pid != player_id}
        message = {
            "action": "deal_cards",
            "player_hand": hands[player_id],
            "opponent_counts": opponent_counts
        }
        try:
            conn.sendall(json.dumps(message).encode())
            print(f"Sent {len(hands[player_id])} cards to player {player_id} with opponents: {opponent_counts}")
        except Exception as e:
            print(f"Error sending cards to player {player_id}: {e}")


def main():
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
        # Accept a new client socket
        conn, addr = server_socket.accept()
        # Start a new thread to handle this client
        thread = threading.Thread(target=client_handler, args=(conn, addr))
        thread.start()


if __name__ == '__main__':
    main()

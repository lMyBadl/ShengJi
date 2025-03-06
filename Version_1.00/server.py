# server.py
import socket  # For network connections
import threading  # To handle multiple clients concurrently
import json  # For encoding/decoding messages in JSON
import random  # To shuffle the deck

# Global list to keep track of connected clients
clients = []


def client_handler(conn, addr):
    """
    Handles communication with a connected client.
    Each client runs in its own thread.
    """
    print(f"New socket from {addr}")
    # Add the new client socket to the global list
    clients.append(conn)

    while True:
        try:
            # Receive data (up to 1024 bytes) from the client
            data = conn.recv(1024)
            if not data:
                # No data indicates the client has disconnected
                break

            # Decode the received bytes to a string and parse the JSON data
            message = json.loads(data.decode())
            print("Received message:", message)

            # Check if the client is requesting to deal cards
            if message.get("action") == "deal_request":
                print("Deal request received; dealing cards...")
                deal_cards(clients)

            # Here you can process other game-related messages as needed.

        except Exception as e:
            print("Error:", e)
            break

    # Remove the client from the list and close the socket when done
    print("Connection closed with", addr)
    if conn in clients:
        clients.remove(conn)
    conn.close()


def deal_cards(client_list):
    """
    Deals out all the cards in a standard deck (52 cards) evenly to all connected clients.

    The deck is represented as a list of strings (e.g., "Ace of Spades"). This function shuffles the deck,
    calculates how many cards each player should receive (assuming an even distribution), and then sends a JSON
    message to each client containing their hand.
    """
    # Define a standard deck of cards
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    deck = [f"{rank} of {suit}" for suit in suits for rank in ranks]

    # Shuffle the deck to randomize card order
    random.shuffle(deck)

    num_players = len(client_list)
    if num_players == 0:
        return

    # Calculate the number of cards per player (for a 52-card deck)
    cards_per_player = len(deck) // num_players
    print(f"Dealing {cards_per_player} cards to each of {num_players} players.")

    # Distribute the cards and send each player's hand
    for i, client in enumerate(client_list):
        # Slice out the hand for this player
        player_cards = deck[i * cards_per_player:(i + 1) * cards_per_player]
        # Build a JSON message that includes the dealt cards
        message = {"action": "deal_cards", "cards": player_cards}
        try:
            client.sendall(json.dumps(message).encode())
        except Exception as e:
            print("Error sending cards to client:", e)


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

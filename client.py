import pygame       # For the GUI
import socket       # For network connections
import json         # To encode/decode messages in JSON
import threading    # To listen for messages concurrently

# Set the IP address and port of your server (replace with your AWS server address)
SERVER_IP = "localhost"
SERVER_PORT = 12345

# Initialize Pygame and set up the window
pygame.init()
screen_width, screen_height = 2000, 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Card Game Client")

# Create a TCP/IP socket and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

player_hand = []

font = pygame.font.SysFont("Arial", 16, bold= True)

def receive_messages():
    """
    Listens for incoming messages from the server in a separate thread.
    """
    global player_hand
    while True:
        try:
            # Receive data from the server (up to 1024 bytes)
            data = client_socket.recv(1024)
            if data:
                # Convert the JSON string to a Python dictionary
                message = json.loads(data.decode())
                print("Received from server:", message)
            if message.get("action") == "deal_cards":
                player_hand = message.get("cards", [])
                print("Player hand updated:", player_hand)
                # Update your game state here based on the received message.
            else:
                # If no data, the server might have closed the connection.
                break
        except Exception as e:
            print("Error receiving data:", e)
            break


def draw_hand(surface, hand):
    """
    Draw the cards in the player's hand at the bottom of the screen.
    Each card is drawn as a white rectangle with a black border and the card name rendered inside.
    """
    # Dimensions for each card representation
    card_width = 100
    card_height = 150
    spacing = 20  # Space between each card

    # Calculate starting x so that cards are centered horizontally
    total_width = len(hand) * card_width + (len(hand) - 1) * spacing
    start_x = (screen_width - total_width) // 2
    y_position = screen_height - card_height - 20  # Position near the bottom with a margin

    # Loop through each card and render it on the screen
    for i, card in enumerate(hand):
        rect_x = start_x + i * (card_width + spacing)
        card_rect = pygame.Rect(rect_x, y_position, card_width, card_height)
        # Draw the card background (white) and border (black)
        pygame.draw.rect(surface, (255, 255, 255), card_rect)
        pygame.draw.rect(surface, (0, 0, 0), card_rect, 2)
        # Render the card text and center it on the card
        card_text = font.render(card, True, (0, 0, 0))
        text_rect = card_text.get_rect(center=card_rect.center)
        surface.blit(card_text, text_rect)


# Start a separate daemon thread for listening to incoming server messages
receive_thread = threading.Thread(target=receive_messages, daemon=True)
receive_thread.start()

# Main game loop
running = True
while running:
    has_deal = False
    for event in pygame.event.get():
        # Handle quitting the game
        if event.type == pygame.QUIT:
            running = False
        # Handle keyboard input (for example, sending a message when space is pressed)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # When space is pressed, send a sample "play_card" action to the server
                message = {"action": "play_card", "card": "Ace of Spades"}
                client_socket.sendall(json.dumps(message).encode())
                print("Sent message to server:", message)
            if has_deal == False:
                if event.key == pygame.K_w:
                    message = {"action": "deal_request"}
                    client_socket.sendall(json.dumps(message).encode())
                    print("Sent message to server deal")
                    has_deal = True



    # Update the screen: fill with a green background (like a card table)
    screen.fill((0, 128, 0))
    # Here you would add drawing code for cards, teams, etc.
    draw_hand(screen, player_hand)
    pygame.display.flip()

# Quit Pygame and close the socket when done
pygame.quit()
client_socket.close()

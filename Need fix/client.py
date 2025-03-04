import pygame
import socket
import json
import threading

# Set up Pygame
pygame.init()
screen_width, screen_height = 2000, 900
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Card Game Client")

# Networking Setup
SERVER_IP = "localhost"
SERVER_PORT = 12345
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

player_hand = []
selected_card_index = None  # Index of the selected card
animating_card = None  # Track which card is being animated
animation_progress = 0  # Progress of animation (0 to 1)
player_id = None
font = pygame.font.SysFont("Arial", 16, bold=True)
opponent_card_counts = {}

def receive_messages():
    global player_hand, selected_card_index, player_id, opponent_card_counts
    while True:
        try:
            data = client_socket.recv(1024)
            if data:
                message = json.loads(data.decode())
                print("Received from server:", message)

                if message.get("action") == "assign_id":
                    player_id = message["player_id"]
                    print(f"Assigned Player ID: {player_id}")

                elif message.get("action") == "deal_cards":
                    player_hand = message["player_hand"]
                    opponent_card_counts = message["opponent_counts"]  # ✅ Store opponent card counts
                    selected_card_index = 0 if player_hand else None
                    print(f"Player hand updated: {player_hand}")
                    print(f"Opponent card counts: {opponent_card_counts}")

        except Exception as e:
            print("Error receiving data:", e)
            break


def draw_opponent_cards(surface, opponent_counts):
    """
    Draws opponents' hands as face-down cards positioned around the screen.
    """
    card_back_image = pygame.image.load("cards/Back Red 1.png").convert_alpha()  # Load a card back image
    card_width, card_height = 80, 120  # Card size
    card_spacing = 20  # Space between cards

    screen_center_x = screen.get_width() // 2
    screen_center_y = screen.get_height() // 2

    opponent_positions = list(opponent_counts.keys())  # Get opponent IDs
    num_opponents = len(opponent_positions)

    # Define fixed positions for up to 3 opponents
    positions = {
        0: (50, screen_center_y - card_height // 2),  # Left side
        1: (screen_center_x - (num_opponents * (card_width + card_spacing)) // 2, 50),  # Top center
        2: (screen.get_width() - 50 - card_width, screen_center_y - card_height // 2),  # Right side
    }

    for i, opponent_id in enumerate(opponent_positions):
        if i >= 3:
            break  # Only handle 3 opponents max for now

        start_x, start_y = positions[i]  # Get correct opponent position

        # Spread out the opponent’s cards
        for j in range(opponent_counts[opponent_id]):
            card_x = start_x + j * (card_width + 5)  # Offset each card slightly
            card_y = start_y

            # If the opponent is on the left or right, stack vertically instead
            if i == 0:  # Left side
                card_x = start_x
                card_y = start_y + j * (card_spacing + 5)
            elif i == 2:  # Right side
                card_x = start_x
                card_y = start_y + j * (card_spacing + 5)

            # Draw the card back
            surface.blit(pygame.transform.scale(card_back_image, (card_width, card_height)), (card_x, card_y))




def draw_glow(surface, position, image):
    """ Creates a glow effect around the selected card. """
    glow_image = pygame.transform.scale(image, (image.get_width() + 20, image.get_height() + 20))
    glow_image.set_alpha(100)  # Transparency (0 = fully transparent, 255 = fully opaque)
    surface.blit(glow_image, (position[0] - 10, position[1] - 10))  # Center glow under card


def draw_hand(surface, hand):
    """ Draws the player's hand, highlighting the selected card with a glow effect. """
    global selected_card_index, animating_card, animation_progress

    card_width = 71
    card_height = 94
    spacing = 5

    total_width = (len(hand) * card_width + (len(hand) - 1) * spacing)
    start_x = (screen_width - total_width) // 2
    y_position = screen.get_height() - card_height - 55

    for i, card in enumerate(hand):
        rect_x = start_x + i * (card_width + spacing)
        rect_x_anim = y_position_anim = 0
        card_rect = pygame.Rect(rect_x, y_position, card_width, card_height)

        # Load card image
        try:
            card_image = pygame.image.load(f"cards/{card}.png").convert_alpha()
            card_image = pygame.transform.scale(card_image, (card_width, card_height))
        except:
            print(f"Error loading image for {card}")
            continue

        # Only move the animating card, leave others in place
        if animating_card == card:
            print(animating_card)
            start_x_anim = start_x + selected_card_index * (card_width + spacing)  # Original position
            target_x, target_y = ((screen_width - card_width )// 2, (screen_height - card_height) // 2)

            rect_x_anim = int(start_x_anim + (target_x - start_x_anim) * animation_progress)
            y_position_anim = int(y_position + (target_y - y_position) * animation_progress)
        else:
            rect_x_anim=rect_x
            y_position_anim = y_position

        # Draw glow effect if the card is selected and not animating
        if selected_card_index == i and animating_card is None:
            draw_glow(surface, (rect_x, y_position), card_image)

        surface.blit(card_image, (rect_x_anim, y_position_anim))

    return start_x, card_width, card_height, spacing


def get_card_at_pos(pos, hand):
    """ Returns the index of the card clicked on, if any. """
    start_x, card_width, card_height, spacing = draw_hand(screen, hand)
    x, y = pos

    y_position = screen.get_height() - card_height - 55

    for i in range(len(hand)):
        rect_x = start_x + i * (card_width + spacing)
        card_rect = pygame.Rect(rect_x, y_position, card_width, card_height)

        if card_rect.collidepoint(x, y):
            return i  # Return index instead of card name
    return None


def animate_card_play(card):
    """ Starts the animation for a played card. """
    global animating_card, animation_progress
    animating_card = card
    animation_progress = 0  # Reset progress


# Start thread for receiving messages
receive_thread = threading.Thread(target=receive_messages, daemon=True)
receive_thread.start()

# Main game loop
running = True
has_deal = False
clock = pygame.time.Clock()

while running:
    screen.fill((0, 128, 0))  # Green background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_index = get_card_at_pos(event.pos, player_hand)
            if clicked_index is not None and animating_card is None:
                selected_card_index = clicked_index
                print(f"Selected Card: {player_hand[selected_card_index]}")

        if event.type == pygame.KEYDOWN and animating_card is None:
            if event.key == pygame.K_LEFT and selected_card_index is not None and selected_card_index > 0:
                selected_card_index -= 1
                print(f"Selected Card: {player_hand[selected_card_index]}")

            if event.key == pygame.K_RIGHT and selected_card_index is not None and selected_card_index < len(
                    player_hand) - 1:
                if selected_card_index == None:
                    selected_card_index = len(player_hand) // 2
                selected_card_index += 1
                print(f"Selected Card: {player_hand[selected_card_index]}")

            if event.key == pygame.K_SPACE and selected_card_index is not None:
                card_to_play = player_hand[selected_card_index]
                animate_card_play(card_to_play)  # Start animation

            if not has_deal and event.key == pygame.K_w:
                message = {"action": "deal_request"}
                client_socket.sendall(json.dumps(message).encode())
                print("Sent message to server deal")
                has_deal = True

    # Handle animation
    if animating_card:
        animation_progress += 0.05  # Adjust speed (higher = faster)
        if animation_progress >= 1:
            # Remove card after animation finishes
            message = {"action": "play_card", "card": animating_card}
            client_socket.sendall(json.dumps(message).encode())
            print("Sent message to server:", message)
            player_hand.remove(animating_card)
            animating_card = None  # Reset animation
           # selected_card_index = max(0, selected_card_index - 1) if player_hand else None

    # Draw updated screen
    draw_hand(screen, player_hand)
    draw_opponent_cards(screen, opponent_card_counts)
    pygame.display.flip()
    clock.tick(60)  # Cap FPS to 60

# Quit Pygame and close the socket
pygame.quit()
client_socket.close()
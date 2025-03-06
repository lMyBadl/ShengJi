import pygame
import socket
import json
import threading
from player import Player

# Set up Pygame
pygame.init()
screenWidth, screenHeight = 2000, 900
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
pygame.display.set_caption("Card Game Client")

# Networking Setup
serverIp = "localhost"
serverPort = 12345
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverIp, serverPort))
dataMultiplier = 4

player = Player()
player.setConnection((serverIp, serverPort))

selectedCardIndex = None  # Index of the selected card
animatingCard = None  # Track which card is being animated
animationProgress = 0  # Progress of animation (0 to 1)
font = pygame.font.SysFont("Arial", 16, bold=True)
opponentCardCounts = {}

def receive_messages():
    global selectedCardIndex, opponentCardCounts, dataMultiplier
    playerHand = player.getHand()
    playerId = player.getId()
    while True:
        try:
            data = clientSocket.recv(1024*dataMultiplier)
            if data:
                message = json.loads(data.decode())
                print("Received from server:", message)

                if message.get("action") == "assign_id":
                    playerId = message["player_id"]
                    print(f"Assigned Player ID: {playerId}")

                elif message.get("action") == "deal_cards":
                    playerHand = message["player_hand"]
                    opponentCardCounts = message["opponent_counts"]  # ✅ Store opponent card counts
                    selectedCardIndex = 0 if playerHand else None
                    print(f"Player hand updated: {playerHand}")
                    print(f"Opponent card counts: {opponentCardCounts}")

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
    global selectedCardIndex, animatingCard, animationProgress

    card_width = 71
    card_height = 94
    spacing = 5

    total_width = (len(hand) * card_width + (len(hand) - 1) * spacing)
    start_x = (screenWidth - total_width) // 2
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
        if animatingCard == card:
            print(animatingCard)
            start_x_anim = start_x + selectedCardIndex * (card_width + spacing)  # Original position
            target_x, target_y = ((screenWidth - card_width) // 2, (screenHeight - card_height) // 2)

            rect_x_anim = int(start_x_anim + (target_x - start_x_anim) * animationProgress)
            y_position_anim = int(y_position + (target_y - y_position) * animationProgress)
        else:
            rect_x_anim=rect_x
            y_position_anim = y_position

        # Draw glow effect if the card is selected and not animating
        if selectedCardIndex == i and animatingCard is None:
            draw_glow(surface, (rect_x, y_position), card_image)

        surface.blit(card_image, (rect_x_anim, y_position_anim))

    return start_x, card_width, card_height, spacing


def getCardAtPos(pos, hand):
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


def animateCardPlay(card):
    """ Starts the animation for a played card. """
    global animatingCard, animationProgress
    animatingCard = card
    animationProgress = 0  # Reset progress





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
            clickedIndex = getCardAtPos(event.pos, playerHand)
            if clickedIndex is not None and animatingCard is None:
                selectedCardIndex = clickedIndex
                print(f"Selected Card: {playerHand[selectedCardIndex]}")

        if event.type == pygame.KEYDOWN and animatingCard is None:
            if event.key == pygame.K_LEFT and selectedCardIndex is not None and selectedCardIndex > 0:
                selectedCardIndex -= 1
                print(f"Selected Card: {playerHand[selectedCardIndex]}")

            if event.key == pygame.K_RIGHT and selectedCardIndex is not None and selectedCardIndex < len(
                    playerHand) - 1:
                if not selectedCardIndex:
                    selectedCardIndex = len(playerHand) // 2
                selectedCardIndex += 1
                print(f"Selected Card: {playerHand[selectedCardIndex]}")

            if event.key == pygame.K_SPACE and selectedCardIndex is not None:
                card_to_play = playerHand[selectedCardIndex]
                animateCardPlay(card_to_play)  # Start animation

            if not has_deal and event.key == pygame.K_w:
                message = {"action": "deal_request"}
                clientSocket.sendall(json.dumps(message).encode())
                print("Sent message to server deal")
                has_deal = True

    # Handle animation
    if animatingCard:
        animationProgress += 0.05  # Adjust speed (higher = faster)
        if animationProgress >= 1:
            # Remove card after animation finishes
            message = {"action": "play_card", "card": animatingCard}
            clientSocket.sendall(json.dumps(message).encode())
            print("Sent message to server:", message)
            playerHand.remove(animatingCard)
            animatingCard = None  # Reset animation
           # selected_card_index = max(0, selected_card_index - 1) if player_hand else None

    # Draw updated screen
    draw_hand(screen, playerHand)
    draw_opponent_cards(screen, opponentCardCounts)
    pygame.display.flip()
    clock.tick(60)  # Cap FPS to 60

# Quit Pygame and close the socket
pygame.quit()
clientSocket.close()
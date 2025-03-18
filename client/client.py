import pygame
import socket
import pickle

from player import Player
from packet import Packet
from button import Button
import platform

#file slash differs between systems to we check that here in order to pull pngs of cards
systemName = platform.system()
if systemName == "linux":
    fileSlash = "/"
else:
    fileSlash = "\\"

#colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Set up Pygame
pygame.init()
screenWidth, screenHeight = 500, 500
window = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
pygame.display.set_caption("Card Game Client")


# Networking Setup
serverIp = "localhost"
serverPort = 12345
dataSize = 1024

player = Player() #creates player object to organize client data

selectedCardIndex = None  # Index of the selected card
animatingCard = None  # Track which card is being animated
animationProgress = 0  # Progress of animation (0 to 1)
font = pygame.font.SysFont("Arial", 16, bold=True)
opponentCardCounts = {}

clock = pygame.time.Clock()
def sendMessage(packet: Packet) -> None:
    """
    :param packet: A packet object to send
    """
    player.getSocket().sendall(pickle.dumps(packet))

def receiveMessage() -> Packet | None:
    """
    Receives a message from the server. If nothing is received, calls the method serverClosed().
    """
    data = player.getSocket().recv(dataSize)
    if not data:
        serverClosed()
        return None
    return pickle.loads(data)

def serverClosed() -> None:
    """
    Quits the client if the server is closed
    """
    pygame.quit()

def loadScreen(screenName: str) -> None:
    """
    Loads the client screen method based on the name of the screen name passed
    :param screenName: The screen name of the button that the client clicked
    """
    if screenName == "Join Random Game":
        joinRandomGame()
    elif screenName == "Load Private Game Lobby":
        privateGameLobby()
    elif screenName == "Create Private Game":
        createPrivateGame()

def joinRandomGame() -> None:
    """
    Opens the join random game screen
    """
    joinMessage = Packet("joinRandom", None)
    try:
        None
    except Exception as e:
        print(e)


def createPrivateGame():
    """
    Opens the private game customizer
    """
    inputFont = pygame.font.SysFont("Arial", 20)
    privateUIFont = pygame.font.SysFont("Arial", 40, bold=True)

    instructionText1 = "Type in the room name. Use the button"
    instructionSurface1 = privateUIFont.render(instructionText1, True, white)
    instructionText2 = "or select the text box and press enter to confirm the name."
    instructionSurface2 = privateUIFont.render(instructionText2, True, white)

    gameName = ""
    inputRectangle = pygame.Rect(window.get_width()//2 - 100, window.get_height()//2 - 15, 200, 30)
    confirmButton = Button("Confirm", privateUIFont, black, white, (200, 100), (window.get_width() // 2 - 100, 3 * window.get_height() // 4 - 50))

    activeColor = pygame.Color("lightskyblue3")
    passiveColor = pygame.Color("gray15")
    color = passiveColor
    active = False

    run = True
    while run:
        clock.tick(60)

        #displaying
        window.fill(black)

        window.blit(instructionSurface1, ((window.get_width() - instructionSurface1.get_width())// 2, (window.get_height() - instructionSurface1.get_height())// 3 - instructionSurface1.get_height()//2))
        window.blit(instructionSurface2, ((window.get_width() - instructionSurface2.get_width()) // 2, (window.get_height() - instructionSurface2.get_height()) // 3 + instructionSurface2.get_height()//2))

        #text box displaying
        inputSurface = inputFont.render(gameName, True, white)
        pygame.draw.rect(window, color, inputRectangle, 4)
        window.blit(inputSurface, (inputRectangle.x + 5, inputRectangle.y + 5))
        inputRectangle.w = max(200, inputSurface.get_width() + 10)
        inputRectangle.x = (window.get_width() - inputRectangle.w)//2
        if active:
            color = activeColor
        else:
            color = passiveColor

        confirmButton.draw(window)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            #checking for typing
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        gameName = gameName[:-1]
                    elif event.key == pygame.K_RETURN:
                        if active:
                            message = Packet("setPrivateGameName", gameName)
                            run = False
                            sendMessage(message)
                    else:
                        gameName += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if confirmButton.isClicked(pos):
                    message = Packet("setPrivateGameName", gameName)
                    run = False
                    sendMessage(message)
                if inputRectangle.collidepoint(pos):
                    active = True
                else:
                    active = False

def privateGameLobby():
    """
    Displays the screen for the list of private games available
    """
    #reload button so that the server doesn't constantly send data
    #layout:
    # 10 px
    # 30 px             title
    # 10 px
    # 2 px              border
    # 16 px (5%) Name(60%)                   Players(20%)     Join Button(10%) (5%)
    # 2 px              border
    # rest of grid
    #join button can change color/pop out if hovered over (check mouse pos every pygame.event, not just when clicked
    rowHeight = 16
    rowBorder = 2
    gridStart = 80
    buttonSize = (window.get_width()//10, rowHeight)

    titleText = "Private Game Lobbies"
    titleFont = pygame.font.SysFont("Arial", 30, bold = True)
    titleTextSurface = titleFont.render(titleText, 1, white)

    #menu column titles
    gameHeader = "Game Name"
    playerHeader = "Players"
    menuFont = pygame.font.SysFont("Arial", 12, bold = True)
    gameHeaderSurface = menuFont.render(gameHeader, 1, white)
    playerHeaderSurface = menuFont.render(playerHeader, 1, white)

    menuBorderRectangle = pygame.Rect(window.get_width()//10, 50, 8*window.get_width()//10, 20)
    playerBorderRectangle = pygame.Rect(2*window.get_width()//10, 50, 2*window.get_width()//10, 20)
    borderRectangles = [menuBorderRectangle, playerBorderRectangle]

    buttonFont = pygame.font.SysFont("Arial", 15, bold = True)

    reloadPrivateGamesButtonText = "Reload"
    joinButton = Button("Join", buttonFont, black, white, buttonSize, (window.get_width()-100, gridStart + rowBorder))
    reloadButton = Button(reloadPrivateGamesButtonText, buttonFont, black, white, buttonSize, ((window.get_width() - buttonSize[0])//2, (window.get_height() - buttonSize[1])//2 - 10))
    buttons = [reloadButton]

    joinButtons = []
    gameIDs = []
    gameNames = []
    playerNumbers = []
    
    displayedGames = []

    active = False
    run = True
    while run:
        window.blit(titleTextSurface, ((window.get_width() - titleTextSurface.get_width())//2, titleTextSurface.get_height()//2 + 10))
        window.blit(gameHeaderSurface, (menuBorderRectangle.x + 2, menuBorderRectangle.y + 2))
        for borderRectangle in borderRectangles:
            pygame.draw.rect(window, white, borderRectangle, 2)

        for button in buttons:
            button.draw(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.isClicked(pos):
                        #gets updated private games list from server
                        if button.getText() == reloadPrivateGamesButtonText:
                            getPrivateGames = Packet("getPrivateGames", 0)
                            sendMessage(getPrivateGames)
                            # Should immediately get back private games
                            packet = receiveMessage()
                            privateGames = packets[0].az;;::
                            numGames = len(privateGames)

                            if window.get_height() - numGames * (2 * rowBorder + rowHeight) - gridStart < 0:
                                numGamesDisplayed = (window.get_height() - gridStart) // (2 * rowBorder + rowHeight)
                            else:
                                numGamesDisplayed = numGames

                            #putting each displayed game in a dictionary so we can access them by their IDs later

                            displayedGames = privateGames[:numGamesDisplayed]

                        if button.getText() == "Join":
                            joinMessage = Packet("joinPrivateGame", displayedGames[buttons.index(button)].getGameID())
                            sendMessage(joinMessage)


        pygame.display.flip()


def inputNameScreen(screenAfter: str):
    """
    Displays a screen for the user to input their name
    :param screenAfter: The screen that the user selected before entering this UI
    """
    global dataSize
    instructionText = "Enter name below:"
    inputFont = pygame.font.SysFont("Arial", 20)
    nameScreenFont = pygame.font.SysFont("Arial", 20)
    confirmButton = Button("Confirm", nameScreenFont, black, white, (200, 100), (window.get_width() // 2 - 100, 3 * window.get_height() // 4 - 50))
    inputText = ""
    inputRectangle = pygame.Rect(window.get_width()//2 - 100, 1*window.get_height()//2 - 15, 200, 30)

    instructionSurface = nameScreenFont.render(instructionText, True, white)
    activeColor = pygame.Color("lightskyblue3")
    passiveColor = pygame.Color("gray15")
    color = passiveColor
    active = False
    run = True
    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((serverIp, serverPort))
        player.setSocket(clientSocket)

        packet = receiveMessage()
        print(f"received from server packets: {str(packet)}")
        if packet.getAction() == "setDataSize":
            dataSize = packet.getValue()

        while run:
            clock.tick(60)
            window.fill(black)

            inputSurface = inputFont.render(inputText, True, white)
            pygame.draw.rect(window, color, inputRectangle, 4)
            window.blit(inputSurface, (inputRectangle.x + 5, inputRectangle.y + 5))
            inputRectangle.w = max(200, inputSurface.get_width() + 10)
            inputRectangle.x = (window.get_width() - inputRectangle.w) // 2
            if active:
                color = activeColor
            else:
                color = passiveColor
            window.blit(instructionSurface, ((window.get_width() - instructionSurface.get_width())//2, (window.get_height() - instructionSurface.get_height())//3))
            confirmButton.draw(window)
            pygame.display.flip()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if confirmButton.isClicked(pos):
                        run = False
                        message = Packet("setPlayerName", inputText)
                        sendMessage(message)
                        loadScreen(screenAfter)
                    if inputRectangle.collidepoint(pos):
                        active = True
                    else:
                        active = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        run = False
                        message = Packet("setPlayerName", inputText)
                        sendMessage(message)
                        loadScreen(screenAfter)
                    if event.key == pygame.K_BACKSPACE:
                        inputText = inputText[:-1]
                    else:
                        inputText += event.unicode
    except Exception as e:
        print(e)

def menuScreen():
    """
    The main screen of the client when starting the application
    """
    run = True
    while run:
        clock.tick(60)
        window.fill(black)

        menuFont = pygame.font.SysFont("Arial", 20)
        joinRandomGameButton = Button("Join Random Game", menuFont, black, white, (200, 100), (window.get_width()//3 - 100, window.get_height()//4 - 50))
        joinPrivateGameButton = Button("Join Private Game", menuFont, black, white, (200, 100), (2*window.get_width()//3 - 100, window.get_height()//4 - 50))
        leaveAppButton = Button("Leave", menuFont, white, red, (200, 100), (window.get_width()//2 - 100, 3*window.get_height()//4 - 50))
        buttons = [joinRandomGameButton, joinPrivateGameButton, leaveAppButton]

        for button in buttons:
            button.draw(window)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.isClicked(pos):
                        run = False
                        buttonText = button.getText()
                        if buttonText == "Leave":
                            pygame.quit()
                        else:
                            inputNameScreen(button.getText())
                            #Yuan is dumb;

menuScreen()



def draw_opponent_cards(surface, opponent_counts):
    """
    Draws opponents' hands as face-down cards positioned around the window.
    """
    card_back_image = pygame.image.load(f"cards{fileSlash}Back Red 1.png").convert_alpha()  # Load a card back image
    card_width, card_height = 80, 120  # Card size
    card_spacing = 20  # Space between cards

    screen_center_x = window.get_width() // 2
    screen_center_y = window.get_height() // 2

    opponent_positions = list(opponent_counts.keys())  # Get opponent IDs
    num_opponents = len(opponent_positions)

    # Define fixed positions for up to 3 opponents
    positions = {
        0: (50, screen_center_y - card_height // 2),  # Left side
        1: (screen_center_x - (num_opponents * (card_width + card_spacing)) // 2, 50),  # Top center
        2: (window.get_width() - 50 - card_width, screen_center_y - card_height // 2),  # Right side
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
    y_position = window.get_height() - card_height - 55

    for i, card in enumerate(hand):
        rect_x = start_x + i * (card_width + spacing)
        rect_x_anim = y_position_anim = 0
        card_rect = pygame.Rect(rect_x, y_position, card_width, card_height)

        # Load card image
        try:
            card_image = pygame.image.load(f"cards{fileSlash}{card}.png").convert_alpha()
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
    start_x, card_width, card_height, spacing = draw_hand(window, hand)
    x, y = pos

    y_position = window.get_height() - card_height - 55

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

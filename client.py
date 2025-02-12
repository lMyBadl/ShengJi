import pygame, sys
from card_logic import Card, Deck
from player import Player

text_size = 50

d = Deck(False)
p = Player()
p2 = Player()
p3 = Player()
p4 = Player()
while len(p4.hand) <= 6:
    p.drawCard(d)
    p2.drawCard(d)
    p3.drawCard(d)
    p4.drawCard(d)

class Durak:
    # Initialize pygame
    pygame.init()
    deck = Deck(False)

    # Screen dimensions
    screen_width = 500
    screen_height = 500

    # Create the screen
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)


    # Set the title of the window
    pygame.display.set_caption("Dark Green Background")
    clock = pygame.time.Clock()
    

    # Define the dark green color (RGB)
    dark_green = (0, 100, 0)

    # Main loop
    running = True
    while running:
                # get all events
        ev = pygame.event.get()

        # proceed events
        for event in ev:

            # handle MOUSEBUTTONUP
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

            # get a list of all sprites that are under the mouse cursor
                # clicked_sprites = [s for s in sprites if s.rect.collidepoint(pos)]
            # do something with the clicked sprites...
            elif event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.size
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)


        # Fill the screen with the dark green color
        screen.fill(dark_green)
        time_surface = pygame.font.Font(None, text_size).render(str(int(clock.get_fps())), True, (255, 255, 255))
        # Position the text in the center of the rectangle
        # text_rect = time_surface.get_rect()

        # Blit (draw) the text onto the screen
        screen.blit(time_surface, (screen_width - text_size, text_size))

        handSize = p.__len__()
        cardShift = 30
        if handSize % 2 == 1:
            #startPos = (screen_width / 2 - int(handSize / 2) * cardShift - cardShift / 2, screen_height - p.getHand()[0].size[1])

            startPos = ((screen_width - p.getHand()[0].size[0])/ 2 - int(handSize/2)*cardShift, screen_height - p.getHand()[0].size[1])
        else:
            #startPos = ((screen_width - p.getHand()[0].size[0])/ 2 - int(handSize/2)*cardShift - cardShift / 2, screen_height - p.getHand()[0].size[1])

            startPos = (screen_width / 2 - int(handSize / 2) * cardShift, screen_height - p.getHand()[0].size[1])

        i=0
        for card in p.getHand():
            screen.blit(card.image, (startPos[0] + cardShift * i, startPos[1]))
            i+=1


        for x in range(p2.__len__()):
            screen.blit(pygame.image.load("Cards Pack\\Large\\Back Blue 2.png"), (startPos[0] + cardShift * x, 0))
            x += 1

        for x in range(p3.__len__()):
            screen.blit(pygame.image.load("Cards Pack\\Large\\Back Blue 2 Horizontal.png"), (0, (screen_width - p.getHand()[0].size[0])/ 2 - int(handSize/2)*cardShift + x * cardShift))



        # Update the display
        clock.tick(60)
        pygame.display.flip()

    # Quit pygame
    pygame.quit()
    sys.exit()

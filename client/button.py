import pygame
class Button:
    def __init__(self, text: str, font, textColor: tuple, buttonColor: tuple, size: tuple, pos: tuple):
        """
        Creates a button
        :param text: text of the button
        :param font: pygame font object for the text font
        :param textColor: color of the text
        :param buttonColor: color of the button
        :param size: size of the button
        :param pos: position of the button
        """
        self.text = text
        self.size = size
        self.pos = pos
        self.font = font
        self.textColor = textColor
        self.buttonColor = buttonColor

    def draw(self, window: pygame.display) -> None:
        """
        Draws the button in the specified window
        :param window: Window in which the button is displayed
        """
        pygame.draw.rect(window, self.buttonColor, self.pos + self.size)
        text = self.font.render(self.text, 1, self.textColor)
        window.blit(text, (self.pos[0] + round(self.size[0] - text.get_width())//2, self.pos[1] + round(self.size[1] - text.get_height())//2))

    def isClicked(self, pos: tuple) -> bool:
        """
        Checks if the button is clicked
        :param pos: The position checked for collision
        :return:
        """
        return self.pos[0] <= pos[0] <= self.pos[0] + self.size[0] and self.pos[1] <= pos[1] <= self.pos[1] + self.size[1]

    def getText(self) -> str:
        """
        Gets the text in the button
        :return: The text of the button
        """
        return self.text

    def setPos(self, pos: tuple) -> None:
        """
        Sets the position of the button
        :param pos: The top left of the button
        """
        self.pos = pos

    def getPos(self) -> tuple:
        """
        Gets the position of the button
        :return: The position of the button
        """
        return self.pos

    def setSize(self, size: tuple) -> None:
        """
        Sets the size of the button
        :param size: The new size of the button
        """
        self.size = size

    def getSize(self) -> tuple:
        """
        Gets the size of the button
        :return: The size of the button
        """
        return self.size
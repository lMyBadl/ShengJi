import socket
from server.shengJi import ShengJi

class Player:
    """
    A player class with its playerSocket and address stored as well for easy accessing
    """
    def __init__(self):
        """
        Initializes a player object with an empty hand, playerNumber, playerSocket, and name
        """
        self.hand = []
        self.playerNumber = None #We don't store either of these b/c I use them as a placeholder when creating the game
        self.playerSocket = None #I set these later when the player actually joins a certain game
        self.name = None
        self.game = None

    def __str__(self):
        output = ""
        for card in self.hand:
            output += str(card) + " "
        return output
        
    def drawCard(self, deck) -> None:
        self.hand.append(deck.drawCard())

    def addCardToHand(self, card):
        self.hand.append(card)

    def playCard(self, card) -> None:
        self.hand.remove(card)

    def getHand(self) -> list:
        return self.hand

    def getCard(self, index: int) -> object:
        return self.hand[index]

    def getID(self) -> int:
        return self.playerNumber

    def setSocket(self, playerSocket: socket):
        """
        :param playerSocket: Socket object
        """
        self.playerSocket = playerSocket

    def getSocket(self) -> socket:
        """
        :return: Socket object
        """
        return self.playerSocket

    def setId(self, playerId: int) -> None:
        self.playerNumber = playerId

    def getName(self) -> str:
        return self.name

    def setName(self, name: str | None) -> None:
        self.name = name

    def getHandSize(self) -> int:
        return len(self.hand)

    def setGame(self, game: ShengJi) -> None:
        self.game = game

    def getGame(self) -> ShengJi:
        return self.game

    #def removeCard(self):

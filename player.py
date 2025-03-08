class Player:
    """
    A player class with its socket and address stored as well for easy accessing
    """
    def __init__(self):
        self.hand = []
        self.playerId = None #We don't store either of these b/c I use them as a placeholder when creating the game
        self.socket = None #I set these later when the player actually joins a certain game

    def __len__(self):
        return self.hand.__len__()

    def __str__(self):
        output = ""
        for card in self.hand:
            output += str(card) + " "
        return output
        
    def drawCard(self, deck) -> None:
        self.hand.append(deck.drawCard())

    def playCard(self, card) -> None:
        self.hand.remove(card)

    def getHand(self) -> list:
        return self.hand

    def getCard(self, index: int) -> object:
        return self.hand[index]

    def getId(self) -> int:
        return self.playerId

    def setSocket(self, socket):
        """
        :param socket: socket object
        """
        self.socket = socket

    def getSocket(self):
        """
        :return: socket object
        """
        return self.socket

    def setId(self, playerId: int):
        self.playerId = playerId

class Player:
    def __init__(self, num: int):
        self.hand = []
        self.num = num

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
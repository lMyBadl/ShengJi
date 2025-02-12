class Player:
    def __init__(self):
        self.hand = []
        
    def drawCard(self, deck):
        self.hand.append(deck.drawCard())

    def playCard(self, card):
        self.hand.remove(card)

    def getHand(self):
        return self.hand

    def __len__(self):
        return self.hand.__len__()

    def __str__(self):
        output = ""
        for card in self.hand:
            output += str(card) + " "
        return output

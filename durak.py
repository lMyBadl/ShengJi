from card_logic import Deck, Card

class Durak:
    def __init__(self):
        self.trumpSuit = None
        self.trumpValue = None
        self.deck = Deck(True, trumpValue, trumpSuit, 2)
        self.deck.shuffleDeck()
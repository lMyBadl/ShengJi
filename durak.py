from card_logic import Deck, Card

class Durak:
    def __init__(self, trumpValue, trumpSuit):
        self.trumpSuit = trumpSuit
        self.trumpValue = trumpValue
        self.deck = Deck(True, trumpValue, trumpSuit, 2)
        self.deck.shuffle()
import random, pygame


validValues = [14, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
validSuits = {"hearts", "diamonds", "spades", "clubs"}


class Card:
    """
    Creates a card object that stores its value and suit
    """
    def __init__(self, value, suit: str, trumpValue: int, trumpSuit: str):
        if self.isValid(value, suit):
            self.value = value
            self.suit = suit
            self.trumpValue = trumpValue
            self.trumpSuit = trumpSuit
            #self.pos = pos
            self.mainSuit = None
            """
            if suit == "clubs": s = "Clubs"
            elif suit == "spades": s = "Spades"
            elif suit == "diamonds": s = "Diamond"
            elif suit == "hearts": s = "Hearts"
            else: s = suit

            if value == 14: v = 1
            else: v = value
            if suit == "joker":
                s = "Joker"
                if value == "red": v = "Red"
                else: v = "Black"
"""
            #self.image = pygame.image.load(f"Cards Pack\\Medium\\{s} {v}.png")
            #self.size = self.image.get_size()
        
        else:
            raise Exception("Invalid value or suit")

    def __lt__ (self, other):
        return other.__gt__(self)

    def __gt__ (self, other):
        #Check Jokers
        if self.suit == "joker":
            if other.suit != "joker":
                return True
            return self.value == "red" and other.value == "black"

        #Check Trump Value
        elif self.value == self.trumpValue:
            if self.suit == self.trumpSuit:
                return other.suit != "joker"
            #dont have trump suit
            return other.suit != other.trumpSuit or other.value != "joker"

        #Check Trump Suit when not having trump value
        elif self.suit == self.trumpSuit:
            if other.suit == other.trumpSuit and other.value != other.trumpValue:
                return self.value > other.value
            #they could have joker or trump value
            return other.value != other.trumpValue or other.suit != "joker"

        #Check Main Suit w/o trump value and trump suit
        elif self.suit == self.mainSuit:
            if other.suit == other.mainSuit and other.value != other.trumpValue:
                return self.value > other.value
            #they could have trump suit, trump value or joker
            return other.value != other.trumpValue or other.suit != other.trumpSuit or other.suit != "joker"

        #if not main suit, trump suit, trump value, or joker then it will always be equal to or smaller
        return False

    def __eq__ (self, other):
        """if self.suit != self.mainSuit and self.suit != self.trumpSuit:
            return other.suit != other.mainSuit and other.suit != other.trumpSuit
        return self.value == other.value and self.suit == other.suit != self.mainSuit"""
        return self.getValue() == other.getValue() and self.getSuit() == other.getSuit()

    def __ne__ (self, other):
        return not self.__eq__(other)

    def __str__(self):
        return f"{self.value} of {self.suit}"
    
    def __repr__(self):
        return f"Card({self.value} of {self.suit})"

    @staticmethod
    def isValid(value, suit: str) -> bool:
        """
        Checks if a card is valid with the given inputs
        :param value: Value of the card
        :param suit: Suit of the card
        :return: True if valid, false if not
        """
        global validValues, validSuits
        if suit == "joker" and value in ["red", "black"]:
            return True
        return value in validValues and suit in validSuits
    """
    def getPos(self) -> tuple:
        return self.pos

    def setPos(self, pos: tuple) -> None:
        self.pos = pos

    def getSize(self) -> tuple:
        return self.size"""

    def getSuit(self) -> str:
        """
        :return: The suit of the card
        """
        return self.suit

    def getValue(self):
        """
        :return: The value of the card
        """
        return self.value

    def setMainSuit(self, suit: str) -> None:
        """
        Sets the main suit of the trick for the comparison method (__gt__)
        :param suit: The main suit
        """
        self.mainSuit = suit

    """def isColliding(self, pos: tuple) -> bool:
        return self.pos[0] <= pos[0] <= self.pos[0] + self.getSize()[0] and self.pos[1] <= pos[1] <= self.pos[1] + self.getSize()[1]
    """
    def setTrumpSuit(self, trumpSuit: str) -> None:
        """
        Sets the trump suit of the card for the comparison method (__gt__)
        """
        self.trumpSuit = trumpSuit

    def setTrumpValue(self, trumpValue: int):
        """
        Sets the trump value of the card for the comparison method (__gt__)
        """
        self.trumpValue = trumpValue

class Deck:
    """
    Creates a deck with the cards being Card objects
    """
    def __init__(self, wantsJokers: bool, numDecks = 1):
        self.wantsJokers = wantsJokers
        self.numDecks = numDecks
        self.trumpSuit = None
        self.trumpValue = None
        self.deck = None

    def __str__(self):
        output = ""
        for card in self.deck:
            output += str(card) + " "
        return output

    def makeDeck(self, trumpValue: int) -> None:
        """
        Creates the actual deck
        :param trumpValue: The trump value of the deck
        """
        global validSuits, validValues
        self.trumpValue = trumpValue
        self.trumpSuit = trumpSuit = "joker"
        self.deck = [Card(value, suit, trumpValue, trumpSuit) for suit in validSuits for value in validValues]
        if self.wantsJokers:
            self.deck.append(Card("red", "joker", trumpValue, trumpSuit))
            self.deck.append(Card("black", "joker", trumpValue, trumpSuit))
        copy = self.deck.copy()
        for i in range(self.numDecks - 1):
            self.deck.extend(copy)

    def getCard(self, index: int) -> Card:
        """
        Returns the card at the specified index
        """
        return self.deck[index]

    def removeCard(self, value, suit: str) -> None:
        """
        Removes a card with the specified value and suit pair
        """
        card = Card(value, suit, self.trumpValue, self.trumpSuit)
        self.deck.remove(card)
    
    def drawCard(self) -> Card:
        """
        Draws a card from the deck and removes that card from the deck
        :return: The card drawn
        """
        return self.deck.pop()
    
    def shuffleDeck(self) -> None:
        """
        Shuffles the deck=
        """
        random.shuffle(self.deck)
    
    def setTrumpSuit(self, trumpSuit: str) -> None:
        """
        Sets the trump suit for the entire deck
        """
        self.trumpSuit = trumpSuit
        for card in self.deck:
            card.setTrumpSuit(trumpSuit)

    def setTrumpValue(self, trumpValue: int) -> None:
        """
        Sets the trump value for the entire deck
        """
        self.trumpValue = trumpValue
        for card in self.deck:
            card.setTrumpValue(trumpValue)

    def setTrump(self, trumpValue: int, trumpSuit: str) -> None:
        """
        Sets both the trump suit and trump value for the entire deck
        """
        self.setTrumpSuit(trumpSuit)
        self.setTrumpValue(trumpValue)
import random, pygame


validValues = [14, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
validSuits = {"hearts", "diamonds", "spades", "clubs"}


class Card:
    def __init__(self, value, suit, trumpValue, trumpSuit, pos = (0, 0)):
        if self.isValid(value, suit):
            self.value = value
            self.suit = suit
            self.trumpValue = trumpValue
            self.trumpSuit = trumpSuit
            self.pos = pos
            self.mainSuit = None
            if suit == "clubs": s = "Clubs"
            elif suit == "spades": s = "Spades"
            elif suit == "diamonds": s = "Diamonds"
            elif suit == "hearts": s = "Hearts"
            else: s = suit

            if value == 14: v = 1
            else: v = value
            if suit == "joker":
                s = "Joker"
                if value == "red": v = "Red"
                else: v = "Black"

            self.image = pygame.image.load(f"Cards Pack\\Medium\\{s} {v}.png")
            self.size = self.image.get_size()
        
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
            #they don't have trump suit but could have joker or trump value
            return other.value != other.trumpValue or other.suit != "joker"

        #Check Main Suit w/o trump value and trump suit
        elif self.suit == self.mainSuit:
            if other.suit == other.mainSuit and other.value != other.trumpValue:
                return self.value > other.value
            #they could have trump suit, trump value or joker
            return other.value != other.trumpValue or other.suit != other.trumpSuit or other.suit != "joker"



        elif self.suit == self.trumpSuit:
            if other.suit != other.trumpSuit:
                return other.value != other.trumpValue or self.value == self.trumpValue
            return self.value == self.trumpValue and other.value != other.trumpValue
        elif self.suit == self.mainSuit:
            if other.suit != other.mainSuit and other.value != other.trumpValue:
                return True
            elif other.suit == other.mainSuit:
                return self.value > other.value
            return
            return self.value == self.trumpValue
        return self.value > other.value

    def __eq__ (self, other):
        return self.value == other.value and self.suit == other.suit

    def __ne__ (self, other):
        return not self.__eq__(other)

    def __str__(self):
        return f"{self.value} of {self.suit}"

    @staticmethod
    def isValid(value, suit):
        global validValues, validSuits
        if suit == "joker" and value in ["red", "black"]:
            return True
        return value in validValues and suit in validSuits

    def getPos(self):
        return self.pos

    def setPos(self, pos: tuple):
        self.pos = pos

    def getSize(self):
        return self.size

    def getSuit(self):
        return self.suit

    def getValue(self):
        return self.value

    def setMainSuit(self, suit):
        self.mainSuit = suit

    def isColliding(self, pos):
        return self.pos[0] <= pos[0] <= self.pos[0] + self.getSize()[0] and self.pos[1] <= pos[1] <= self.pos[1] + self.getSize()[1]


class Deck:
    def __init__(self, wantsJokers, numDecks = 1):

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

    def makeDeck(self):
        global validSuits, validValues
        self.deck = [Card(value, suit, self.trumpValue, self.trumpSuit) for suit in validSuits for value in validValues]
        if self.wantsJokers:
            self.deck.append(Card("red", "joker"))
            self.deck.append(Card("black", "joker"))
        copy = self.deck.copy()
        for i in range(self.numDecks - 1):
            self.deck.extend(copy)

    def getCard(self, index):
        return self.deck[index]

    def removeCard(self, value, suit):
        card = Card(value, suit)
        if card not in self.deck:
            return False
        self.deck.remove(card)
        return True
    
    def drawCard(self):
        return self.deck.pop()
    
    def shuffleDeck(self):
        random.shuffle(self.deck)
    
    def setTrumpSuit(self, trumpSuit):
        self.trumpSuit = trumpSuit

    def setTrumpValue(self, trumpValue):
        self.trumpValue = trumpValue

    def setTrump(self, trumpSuit, trumpValue):
        self.setTrumpSuit(trumpSuit)
        self.setTrumpValue(trumpValue)
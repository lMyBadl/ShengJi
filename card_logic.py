import random, pygame
#default deck without jokers for checking
validValues = [14, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13] #in case we haven't converted to ints yet
#red = 1 and black = 2 because I don't want to bother adding another thing just for colors

#five suits for us, hearts, diamonds, spades, clubs, and JOKERS
validSuits = {"hearts", "diamonds", "spades", "clubs"}


class Card:
    def __init__(self, value, suit, trumpValue, trumpSuit, pos = (0, 0)):
        if self.isValid(value, suit):
            self.value = value
            self.suit = suit
            self.trumpSuit = trumpSuit
            self.trumpValue = trumpValue
            self.pos = pos
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
                elif value == "black": v = "Black"

            self.image = pygame.image.load(f"Cards Pack\\Large\\{s} {v}.png")
            self.size = self.image.get_size()
        
        else:
            raise Exception("Invalid value or suit")

    def __lt__ (self, other):
        return other.__gt__(self)

    def __gt__ (self, other):
        if self.suit == "joker":
            if other.suit != "joker":
                return True
            return self.value == "red" and other.value == "black"
        elif self.suit == self.trumpSuit and other.suit != other.trumpSuit:
            if other.suit != other.trumpSuit:
                return other.value != other.trumpValue or self.value == self.trumpValue
            return self.value == self.trumpValue and other.value != other.trumpValue
        elif self.suit != self.trumpSuit:
            return self.value == self.trumpValue
        return self.value > other.value

    def __eq__ (self, other):
        return self.value == other.value and self.suit == other.suit

    def __ne__ (self, other):
        return not self.__eq__(other)

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

    def __str__(self):
        return f"{self.value} of {self.suit}"


class Deck:
    def __init__(self, wantsJokers, trumpValue, trumpSuit, numDecks = 1):
        global validSuits, validValues
        self.wantsJokers = wantsJokers
        self.numDecks = numDecks
        self.trumpSuit = trumpSuit
        self.trumpValue = trumpValue
        self.deck = [Card(value, suit, trumpValue, trumpSuit) for suit in validSuits for value in validValues]
        if wantsJokers:
            self.deck.append(Card("red", "joker", trumpSuit, trumpValue))
            self.deck.append(Card("black", "joker", trumpSuit, trumpValue))
        copy = self.deck.copy()
        for i in range(numDecks - 1):
            self.deck.extend(copy)

    def getCard(self, index):
        return self.deck[index]

    def removeCard(self, value, suit):
        card = Card(value, suit, self.trumpValue, self.trumpSuit)
        if card not in self.deck:
            return False
        self.deck.remove(card)
        return True
    
    def drawCard(self):
        return self.deck.pop()
    
    def shuffleDeck(self):
        random.shuffle(self.deck)
    
    def __str__(self):
        output = ""
        for card in self.deck:
            output += str(card) + " "
        return output

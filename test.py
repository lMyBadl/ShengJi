from packet import Packet
from shengJi import ShengJi
game = ShengJi(1)
game.setTrumpSuit("hearts")
deck = game.deck
print(deck)
print(game.deck)
deck.shuffleDeck()
print(deck)
print(game.deck)
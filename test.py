from packet import Packet
from server.card_logic import Card

card1 = Card(2, "hearts", -1, "")
card2 = Card(2, "diamonds", -1, "")
card3 = Card("red", "joker", -1, "")
card4 = Card("black", "joker", -1, "")
print(card1 > card2)
print(card2 > card1)
print(card3 > card1)
print(card4 > card1)
print(card4 > card3)
print(card3 > card4)


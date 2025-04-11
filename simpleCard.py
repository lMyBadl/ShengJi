class SimpleCard:
    """
    A very basic card object for the client
    """
    def __init__(self, value, suit: str):
        """
        :param value: The value of the card
        :param suit: The suit of the card
        """
        self.value = value
        self.suit = suit

    def __str__(self):
        return [self.value, self.suit]

    def __eq__(self, other):
        return self.getValue() == other.getValue() and self.getSuit() == other.getSuit()

    def getValue(self):
        """
        Gets the value of the card
        :return: Value of the card
        """
        return self.value

    def getSuit(self) -> str:
        """
        Gets the suit of the card
        :return: Suit of the card
        """
        return self.suit

    def setValue(self, value) -> None:
        """
        Sets the value of the card
        :param value: New value of the card
        """
        self.value = value

    def setSuit(self, suit: str) -> None:
        """
        Sets the suit of the card
        :param suit: New suit of the card
        """
        self.suit = suit
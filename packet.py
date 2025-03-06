class Packet:
    def __init__(self, action: str, value):
        """
        sends an action-value pair encased as an object
        Client send options: playCard, getCardNumbers, setGameName, setReady, setPlayerName
        Server send options: assignId, setDataSize
        """
        self.action = action
        self.value = value

    def __str__(self):
        return f"{self.action}:{self.value}"

    def getValue(self):
        return self.value

    def getAction(self):
        return self.action
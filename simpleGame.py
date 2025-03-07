class SimpleGame:
    def __init__(self, name: str, numPlayers: int, gameID: int):
        self.name = name
        self.numPlayers = numPlayers
        self.gameID = gameID

    def getName(self) -> str:
        return self.name

    def getNumPlayers(self) -> int:
        return self.numPlayers

    def getGameID(self) -> int:
        return self.gameID
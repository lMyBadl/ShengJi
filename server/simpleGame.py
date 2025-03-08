class SimpleGame:
    """
    A simplified ShengJi object with only the information that the client needs.
    """
    def __init__(self, name: str, numPlayers: int, gameID: int):
        self.name = name
        self.numPlayers = numPlayers
        self.gameID = gameID #Game ID is important because if two games are the same then we have no idea which game the client is referring to

    def getName(self) -> str:
        return self.name

    def getNumPlayers(self) -> int:
        return self.numPlayers

    def getGameID(self) -> int:
        return self.gameID
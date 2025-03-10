from card_logic import Deck
from player import Player
class ShengJi:
    """
    An object which controls the logic and rules behind the card game "ShengJi", aka Tractor or Finding Friends
    """
    def __init__(self, gameId: int):
        self.name = None
        self.trumpSuit = None

        self.gameID = gameId
        self.ready = False
        self.players = [Player(), Player(), Player(), Player()]
        self.playersWent = [False, False, False, False]

        self.level = 2
        self.deck = Deck(True, 2)
        self.deck.setTrumpValue(self.level)
        self.playerPoints = [0, 0, 0, 0]

        self.moves = [[], [], [], []]
        self.trickStarter = 0


    def play(self, player: int, move: list):
        """
        :param player: [0, 1, 2, 3]
        :param move: The Player's move from an array of Card objects
        """
        self.moves[player] = move
        self.playersWent[player] = True

    def setTrickStarter(self, player: int):
        self.trickStarter = player

    @staticmethod
    def getNextPlayer(player: int) -> int:
        if player == 3:
            return 0
        return player + 1

    def getTrickWinner(self) -> int:
        """
        :return: Index of the winning player
        """
        winner = self.trickStarter
        mainSuit = self.moves[winner][0].getSuit()
        nextPlayer = self.getNextPlayer(winner)
        #setting main suit for the played cards
        for playerMove in self.moves:
            for card in playerMove:
                card.setMainSuit(mainSuit)

        for _ in range(3):
            if len(self.moves[winner]) == 1:
                if self.moves[winner][0] < self.moves[nextPlayer][0]:
                    winner = nextPlayer
            elif len(self.moves[winner]) == 2:
                if self.moves[self.getNextPlayer(winner)][0] == self.moves[nextPlayer][1] and self.moves[winner][0] < self.moves[nextPlayer][0]:
                    winner = nextPlayer
            nextPlayer = self.getNextPlayer(nextPlayer)
        return winner

    def getPointsInTrick(self) -> int:
        points = 0
        for playerMove in self.moves:
            for card in playerMove:
                if card.getValue() == 13 or 10:
                    points += 10
                elif card.getValue() == 5:
                    points += 5
        return points

    def getPlayerMove(self, player: int):
        """
        :param player: [0, 1, 2, 3]
        :return: The player's move
        """
        return self.moves[player]

    def playPlayerMove(self, player: int, move: list):
        self.moves[player] = move
        self.playersWent[player] = True

    def allPlayed(self) -> bool:
        return self.playersWent[0] and self.playersWent[1] and self.playersWent[2] and self.playersWent[3]

    def setTrumpSuit(self, suit: str):
        self.trumpSuit = suit

    def getTrumpSuit(self) -> str:
        return self.trumpSuit

    def setLevel(self, level: int):
        self.level = level

    def setReady(self, ready: bool):
        self.ready = ready

    def allReady(self) -> bool:
        return self.ready

    def getPlayerFromId(self, playerId: int):
        for player in self.players:
            if player.getID() is playerId:
                return player
        raise Exception(f"Player id {playerId} not found.")

    def getPlayerFromIndex(self, index: int):
        return self.players[index]

    def getPlayerFromName(self, name: str):
        for player in self.players:
            if player.name == name:
                return player
        return None

    def setName(self, name: str):
        self.name = name

    def getName(self) -> str:
        return self.name

    def addPointsToPlayer(self, points: int, playerNum: int):
        """
        :param points: Integer of points added
        :param playerNum: Index of player [0, 1, 2, 3]
        """
        self.playerPoints[playerNum] += points

    def addNewPlayer(self, player) -> int:
        """

        :param player: The player object to add
        :return: 0, 1, 2, or 3 if player is added, -1 if unavailable
        """
        for i in range(4):
            if not self.players[i].getName():
                self.players[i] = player
                return i
        return -1

    def isFilled(self):
        return self.players[0].getName() and self.players[1].getName() and self.players[2].getName() and self.players[3].getName()

    def getID(self):
        return self.gameID

    def getPlayersJoined(self):
        count = 0
        for player in self.players:
            if player.getName(): #if player has a name
                count += 1
        return count

    def getPlayerIndex(self, player):
        return self.players.index(player)
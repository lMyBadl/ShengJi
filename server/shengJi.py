from card_logic import Deck
from player import Player
class ShengJi:
    """
    An object which controls the logic and rules behind the card game "ShengJi", aka Tractor or Finding Friends
    """
    def __init__(self, gameId: int):
        self.name = None
        self.gameID = gameId

        self.ready = [False, False, False, False]
        self.players = [Player(), Player(), Player(), Player()]
        self.playersWent = [False, False, False, False]

        self.trumpSuit = None
        self.level = 2
        self.deck = Deck(True, 2)
        self.deck.makeDeck(self.level)
        self.deck.setTrumpValue(self.level)
        self.playerPoints = [0, 0, 0, 0]

        self.moves = [[], [], [], []]
        self.trickStarter = 0
        self.trickSize = 1
        self.attackingTeam = 0
        self.colorOfTrumpSuitIfJoker = None

    def reset(self) -> str:
        self.ready = [False, False, False, False]
        self.players = [Player(), Player(), Player(), Player()]
        self.playersWent = [False, False, False, False]

        self.trumpSuit = None
        self.level = 2
        self.deck = Deck(True, 2)
        self.deck.makeDeck(self.level)
        self.deck.setTrumpValue(self.level)
        self.playerPoints = [0, 0, 0, 0]

        self.moves = [[], [], [], []]
        self.trickStarter = 0
        self.trickSize = 1
        self.attackingTeam = 0
        self.colorOfTrumpSuitIfJoker = None
        return "Reset Game"

    def playCard(self, player: int, move) -> None:
        """

        :param player: [0, 1, 2, 3]
        :param move: The Player's move as either a single item or an array of items
        """
        self.moves[player] = move
        self.playersWent[player] = True

    def setTrumpSuit(self, trumpSuit: str) -> None:
        """
        Sets the trump suit for the deck in the game
        """
        self.trumpSuit = trumpSuit
        self.deck.setTrumpSuit(trumpSuit)

    def setTrickStarter(self, playerIndex: int):
        self.trickStarter = self.getPlayerIndex(playerIndex)

    def getTrickStarter(self) -> int:
        return self.trickStarter

    def levelUp(self):
        self.level += 1

    def drawCard(self):
        return self.deck.drawCard()
    
    def getDeck(self):
        return self.deck

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

    def allPlayed(self) -> bool:
        return self.playersWent[0] and self.playersWent[1] and self.playersWent[2] and self.playersWent[3]

    def getTrumpSuit(self) -> str:
        return self.trumpSuit

    def setLevel(self, level: int):
        self.level = level

    def setPlayerReady(self, player: Player, ready: bool):
        playerIndex = self.getPlayerIndex(player)
        self.ready[playerIndex] = ready

    def allReady(self) -> bool:
        return self.ready[0] and self.ready[1] and self.ready[2] and self.ready[3]

    def getNumPlayersReady(self):
        count = 0
        for x in self.ready:
            if x:
                count += 1

        return count

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

    def getNumPlayersJoined(self):
        count = 0
        for player in self.players:
            if player.getName(): #if player has a name
                count += 1
        return count

    def getPlayerIndex(self, player):
        return self.players.index(player)
    
    def getPlayers(self):
        return self.players

    def getLevel(self) -> int:
        return self.level

    def changeAttackingTeam(self) -> None:
        if self.attackingTeam == 0:
            self.attackingTeam = 1
        else:
            self.attackingTeam = 0

    def getAttackingTeam(self) -> int:
        """
        :return: Team 0 (player0 & player 2), or team 1 (player1 & player 3)
        """
        return self.attackingTeam

    def setAttackingTeam(self, player):
        """
        :param player: The player that set the trump suit in dealing
        """
        playerIndex = self.getPlayerIndex(player)
        if playerIndex == 0 or 2:
            self.attackingTeam = 0
        else:
            self.attackingTeam = 1

    def setColorOfTrumpSuitIfJoker(self, color:str):
        self.colorOfTrumpSuitIfJoker = color

    def getColorOfTrumpSuitIfJoker(self) -> str:
        return self.colorOfTrumpSuitIfJoker
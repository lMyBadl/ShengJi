class ShengJi:
    def __init__(self, gameId: int):
        self.trumpSuit = None

        self.gameId = gameId
        self.ready = False
        self.playersWent = [False, False, False, False]

        self.level = 2
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

    def getTrickWinner(self) -> int:
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

    @staticmethod
    def getNextPlayer(player: int) -> int:
        if player == 3:
            return 0
        return player + 1

    def getPlayerMove(self, player: int):
        """
        :param player: [0, 1, 2, 3]
        :return: The player's move
        """
        return self.moves[player]

    def playPlayerMove(self, player: int, move: list):
        self.moves[player] = move
        self.playersWent[player] = True

    def allReady(self) -> bool:
        return self.playersWent[0] and self.playersWent[1] and self.playersWent[2] and self.playersWent[3]

    def setTrumpSuit(self, suit: str):
        self.trumpSuit = suit

    def getTrumpSuit(self) -> str:
        return self.trumpSuit

    def setLevel(self, level: int):
        self.level = level
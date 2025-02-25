class Durak:
    def __init__(self, gameId, trumpSuit, level):
        self.trumpSuit = trumpSuit

        self.gameId = gameId
        self.ready = False
        self.playersWent = [False, False, False, False]

        self.level = level
        self.moves = [[], [], [], []]
        self.trickStarter = 0

    def play(self, player, move):
        self.moves[player] = move
        self.playersWent[player] = True

    def setTrickStarter(self, player):
        self.trickStarter = player

    def getTrickWinner(self):
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

    def getPointsInTrick(self):
        points = 0
        for playerMove in self.moves:
            for card in playerMove:
                if card.getValue() == 13 or 10:
                    points += 10
                elif card.getValue() == 5:
                    points += 5
        return points

    @staticmethod
    def getNextPlayer(player):
        if player == 3:
            return 0
        return player + 1

    def getPlayerMove(self, player):
        """
        :param player: [0, 1, 2, 3]
        :return: The player's move
        """
        return self.moves[player]

    def playPlayerMove(self, player, move):
        self.moves[player] = move
        self.playersWent[player] = True

    def allReady(self):
        return self.playersWent[0] and self.playersWent[1] and self.playersWent[2] and self.playersWent[3]
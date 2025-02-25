class Durak:
    def __init__(self, id, trumpSuit):
        self.trumpSuit = trumpSuit

        self.id = id
        self.ready = False
        self.playersWent = [False, False, False, False]

        self.teamLevel = [2,2]
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
        for i in range(3):
            if self.moves[winner].__len__() == 2:
                if self.moves[winner] <

            if self.moves[self.trickStarter][0] == self.trumpSuit:

        return winner

    def getPlayerMove(self, player):
        """
        :param player: [0, 1, 2, 3]
        :return: The player's move
        """
        return self.moves[player]

class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0,0]
        self.ties = 0

    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False
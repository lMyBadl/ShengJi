class Packet:
    def __init__(self, action: str, value):
        """
        Encases an action-value pair as an object
        """
        """                  
        Client Actions:   
        what client sends               -> what server sends back
        
            First join:
        setPlayerName (name)            -> gotPlayerName (name)
        
            Waiting in menu screen:
        setPrivateGameName (gameName)   -> createdNewPrivateGame (gameName)
        getPrivateGames ("")            -> returnPrivateGames (list of simplified private games)
        joinPrivateGame (gameID)        -> if joined: joinedPrivateGame (gameID) else: failedToJoinPrivateGame (reason)
        joinRandomGame ("")             -> joinedRandomGame (gameID)
        
            During game:
        setTrumpSuit ([value, suit])    -> changedTrumpSuit (suit) or if not valid invalidCard ("")
        
        Server Actions:
        what server sends               -> what client sends back
        
            First join:
        setDataSize (size)              -> gotDataSize (size)
        
            Joining a game:
        assignID (playerID)             -> gotPlayerID (playerID)
        
            Waiting in game lobby:
        setTotalPlayers (numPlayers)    -> gotTotalPlayers (numPlayers)
        startingGame ("")               -> readyToPlay (playerName)
        #can be implemented
        playerReady (playerName)        -> gotPlayerReady (playerName)
        playerUnready (playerName)      -> gotPlayerUnready (playerName)

            Drawing cards:
        addCardToHand (card)            -> addedCardToHand (card)
        """
        self.action = action
        self.value = value

    def __str__(self):
        return f"{self.action}:{self.value}"

    def __repr__(self):
        return f"Packet({self.action}, {self.value})"

    def getValue(self):
        return self.value

    def getAction(self):
        return self.action
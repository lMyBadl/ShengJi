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
        
            Waiting in lobby:
        setPrivateGameName (gameName)   -> createNewPrivateGame (gameName)
        getPrivateGames ("")            -> returnPrivateGames (list of simplified private games)
        joinPrivateGame (gameID)        -> if joined: joinedPrivateGame (gameID) else: failedToJoinPrivateGame (reason)
        joinRandomGame ("")             -> joinedRandomGame (gameID)
        
        Server Actions:
        what server sends               -> what client sends back
        
            First join:
        setDataSize (size)              -> gotDataSize (size)
        
            Joining a game:
        assignID (playerID)             -> gotPlayerID (playerID)
        
        Client send options: playCard, getCardNumbers, setReady, setPlayerName
        Server send options: assignId, setDataSize
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
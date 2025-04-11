class Packet:
    def __init__(self, action: str, value = ""):
        """
        Encases an action-value pair as an object
        """
        """                  
        Client Actions:   
        what client sends               -> what server sends back
        
            First join:
        set player name (name)          -> got player name (name)
        
            Waiting in menu screen:
        create private game (gameName)  -> created new private game (gameName)
        get private games ("")          -> return private games (list of simplified private games)
        join private game (gameID)        -> if joined: joined private game (gameID) 
                                            else: failed to join private game (reason)
        join random game ("")             -> joinedRandomGame (gameID)
        
            During game:
        set trump suit ([value, suit])    -> set trump suit (suit)
                                            reinforced trump suit (suit)
                                            changed trump suit (suit)
                                            or if not valid invalid card ("")
        ready to play ("")                -> got ready to play ("")
        play cards (simple card(s))      -> got cards (simple card(s))
        
        Server Actions:
        what server sends               -> what client sends back
        
            First join:
        set data size (size)              -> got data size (size)
        
            Joining a game:
        assign ID (playerID)             -> got player ID (playerID)
        
            Waiting in game lobby:
        set total players (numPlayers)    -> got total players (numPlayers)
        starting game ("")               -> ready to play (playerName)
        
        #can be implemented
        player ready (playerName)        -> got player ready (playerName)
        player unready (playerName)      -> got player unready (playerName)

            Drawing cards:
        add card to hand (card)            -> added card to hand (card)
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
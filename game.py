class Game():
    def __init__(self):
        self.started = False
        self.players = {}

    def addPlayer(self, ctx)->bool:
        if(self.started): return False
        
        name = ctx.author.name
        if(name in self.players): return False

        self.players[name] = ctx
        return True
        

    def removePlayer(self, name)->bool:
        if(self.started): return False

        if(name in self.players):
            del self.players[name]
            return True
        return False
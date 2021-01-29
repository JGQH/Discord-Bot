from player import Player
from discord.ext import commands

class Game():
    def __init__(self):
        self.started = False
        self.players = {}

    def addPlayer(self, ctx:commands.Context)->bool:
        if(self.started): return False
        
        name = ctx.author.name
        if(self.playerExists(name)): return False

        self.players[name] = Player(ctx)
        return True
        

    def removePlayer(self, name:str)->bool:
        if(self.started): return False

        if(self.playerExists(name)):
            del self.players[name]
            return True
        return False

    def playerExists(self, name:str)->bool:
        return (name in self.players)

    async def startGame(self):
        if(len(self.players) == 1):
            print("Game has started!")
            for name in self.players:
                player:Player = self.players[name]
                await player.ctx.send("Game has started!")
            self.started = True
from discord.ext import commands

class Player():
    def __init__(self, ctx:commands.Context):
        self.ctx = ctx
        self.hp = 3
        self.rotation = 0
        self.x = 0
        self.y = 0
        self.actionsUsed = 0
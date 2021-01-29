from discord.ext import commands

class Player():
    def __init__(self, ctx:commands.Context):
        self.ctx = ctx
        self.hp = 3
        self.x, self.y = 0, 0
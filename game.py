from player import Player
from discord.ext import commands
from threading import Timer
from module import getMove, loopVal
from timer import Timer
import random
import math

class Game():
    MIN_PLAYER_COUNT = 1
    ROUND_DURATION = 15

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
        if(len(self.players) == Game.MIN_PLAYER_COUNT):
            print("Game has started!")
            for name in self.players:
                player:Player = self.players[name]
                await player.ctx.send("Game has started!")

            self.randomizePositions()
            self.resetActions()
            self.started = True

    def addAction(self, name:str, action:str, val:None)->str:
        player:Player = self.players[name]

        if((player.actionsUsed < 3) and (action in ["move", "shoot", "rotate"])):
            self.actions[player.actionsUsed][action][name] = val
            player.actionsUsed += 1

            return f'Action succesfully added (Used actions: {player.actionsUsed}/3)'
        return "Action couldn't be validated"

    def resetActions(self):
        self.actions = [{
            "move": {},
            "shoot": {},
            "rotate": {}
        }, {
            "move": {},
            "shoot": {},
            "rotate": {}
        }, {
            "move": {},
            "shoot": {},
            "rotate": {}
        }]

        self.timer = Timer(Game.ROUND_DURATION, self.doGame)

    async def doGame(self):
        #Action priority: move > shoot > rotate
        for i in range(3):
            actions = self.actions[i]

            #Execute actions
            self.playerMove(actions["move"])

            self.playerShoot(actions["shoot"])

            self.playerRotate(actions["rotate"])

            await self.killPlayers()

        self.resetActions()
        await self.updatePlayers()

    def playerMove(self, actions:dict):
        for name in actions:
            player:Player = self.players[name]
            dx, dy = getMove(actions[name])

            player.x = loopVal(player.x + dx)
            player.y = loopVal(player.y + dy)

    def playerShoot(self, actions:dict):
        for name in actions:
            player:Player = self.players[name]
            rad = math.pi * player.rotation / 180

            x = player.x
            y = player.y

            while ((0 < x < 40) and (0 < y < 40)):
                x += math.cos(rad)
                y += math.sin(rad)

                target = self.getPlayerAt(int(x), int(y))
                if(target):
                    target.hp -= 1

    def playerRotate(self, actions:dict):
        for name in actions:
            try:
                player:Player = self.players[name]
                rotation = int(actions[name])
                player.rotation = (player.rotation + rotation) % 360
            except:
                pass

    def randomizePositions(self):
        for name in self.players:
            player:Player = self.players[name]

            notPlaced = True
            while notPlaced:
                rndX = random.randrange(0, 40)
                rndY = random.randrange(0, 40)

                if(self.getPlayerAt(rndX, rndY)):
                    pass
                else:
                    player.x = rndX
                    player.y = rndY
                    notPlaced = False

    def getPlayerAt(self, x:int, y:int):
        for name in self.players:
            player:Player = self.players[name]
            if((player.x == x) and (player.y == y)):
                return player
        return

    async def updatePlayers(self):
        for name in self.players:
            player:Player = self.players[name]
            player.actionsUsed = 0
            await player.ctx.send(f'You can move now. Location: ({player.x}, {player.y})')

    async def killPlayers(self):
        for name in self.players:
            player:Player = self.players[name]
            if(player.hp <= 0):
                #Removes player's remaining actions
                for i in range(1, 3):
                    actions = self.actions[i]
                    actions["move"].pop(name, None)
                    actions["shoot"].pop(name, None)
                    actions["rotate"].pop(name, None)

                #Removes player from player list
                del self.players[name]
                await player.ctx.send("You've been killed!")

        if(len(self.players) == 0):
            self.started = False
            self.timer.cancel()
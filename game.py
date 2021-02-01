from player import Player
from drawer import Drawer
from discord.ext import commands
from discord import File as DFile
from module import getMove, loopVal
from timer import Timer
import random
import math

class Game():
    MAX_BOARD_SIZE = 15
    MIN_PLAYER_COUNT = 2
    ROUND_DURATION = 25 #Measured in seconds

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
            self.randomizePositions()

            for name in self.players:
                player:Player = self.players[name]
                await player.ctx.send("Game has started!")
                
            await self.updatePlayers()
            self.resetActions()
            self.started = True

    def addAction(self, name:str, action:str, val:None)->str:
        player:Player = self.players[name]

        if((player.actionsUsed < 3) and (action in ["move", "shoot", "aim"])):
            self.actions[player.actionsUsed][action][name] = val
            player.actionsUsed += 1

            return f'Action succesfully added (Used actions: {player.actionsUsed}/3)'
        return "Action couldn't be validated"

    def resetActions(self):
        self.actions = [{
            "move": {},
            "shoot": {},
            "aim": {}
        }, {
            "move": {},
            "shoot": {},
            "aim": {}
        }, {
            "move": {},
            "shoot": {},
            "aim": {}
        }]

        self.timer = Timer(Game.ROUND_DURATION, self.doGame)

    async def doGame(self):
        #Action priority: move > shoot > aim
        for i in range(3):
            actions = self.actions[i]

            #Execute actions
            self.playerMove(actions["move"])

            self.playerShoot(actions["shoot"])

            self.playerAim(actions["aim"])

            await self.killPlayers()

        self.resetActions()
        await self.updatePlayers()

    def playerMove(self, actions:dict):
        for name in actions:
            player:Player = self.players[name]
            dx, dy = getMove(actions[name])

            player.x = loopVal(player.x + dx, Game.MAX_BOARD_SIZE)
            player.y = loopVal(player.y + dy, Game.MAX_BOARD_SIZE)

    def playerShoot(self, actions:dict):
        for name in actions:
            player:Player = self.players[name]
            rad = math.pi * player.rotation / 180

            x = player.x
            y = player.y

            nx = x
            ny = y
            while ((0 < x < Game.MAX_BOARD_SIZE) and (0 < y < Game.MAX_BOARD_SIZE)):
                nx += math.cos(rad)
                ny -= math.sin(rad)

                if((int(nx) != x) or (int(ny) != y)):
                    x = int(nx)
                    y = int(ny)

                    target = self.getPlayerAt(x, y)
                    if(target):
                        target.hp -= 1
                        break

    def playerAim(self, actions:dict):
        for name in actions:
            try:
                player:Player = self.players[name]
                rotation = int(actions[name])
                player.rotation = rotation % 360
            except:
                pass

    def randomizePositions(self):
        for name in self.players:
            player:Player = self.players[name]

            notPlaced = True
            while notPlaced:
                rndX = random.randrange(0, Game.MAX_BOARD_SIZE)
                rndY = random.randrange(0, Game.MAX_BOARD_SIZE)

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
        board = Drawer.renderBoard(self.players)
        if len(self.players == 1):
            for name in self.players:
                player:Player = self.players[name]
                await player.ctx.send(content="You've won")
                
            self.started = False
            self.timer.cancel()
        else:
            for name in self.players:
                player:Player = self.players[name]
                player.actionsUsed = 0

                new_board = Drawer.renderPlayer(player, board)
                await player.ctx.send(content="Actions update, current board:", file=new_board)
            print("\nNew round!")

    async def killPlayers(self):
        for name in self.players:
            player:Player = self.players[name]
            if(player.hp <= 0):
                #Removes player's remaining actions
                for i in range(1, 3):
                    actions = self.actions[i]
                    actions["move"].pop(name, None)
                    actions["shoot"].pop(name, None)
                    actions["aim"].pop(name, None)

                #Removes player from player list
                del self.players[name]
                await player.ctx.send("You've been killed!")
            
        
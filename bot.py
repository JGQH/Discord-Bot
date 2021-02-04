import os
from dotenv import load_dotenv
from discord.ext import commands
from game import Game
from drawer import Drawer
from player import Player

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

botto = commands.Bot(command_prefix='!')

Drawer.loadImgs(Game.MAX_BOARD_SIZE)
game = Game()

#Events
@botto.event
async def on_ready():
    print(f'{botto.user.name} is alive!')

@botto.command(name='howto', help='Displays a message about how to play')
async def howto(ctx:commands.Context):
    await ctx.send(open("resources/how_to.txt").read())

@botto.command(name='join', help='Allows a new player to join the current game')
async def join(ctx:commands.Context):
    if(game.addPlayer(ctx)):
        name = ctx.author.name
        await ctx.send(f'Welcome aboard, {name}!')
        print(f'Player {name} joined the game!')

        await game.startGame()
    else:
        await ctx.send("We couldn't add you to the game!")

@botto.command(name='leave', help='Removes player from game if it hasn\'t started yet')
async def leave(ctx:commands.Context):
    name = ctx.author.name
    if(game.removePlayer(name)):
        await ctx.send(f'Until next time, {name}!')
        print(f'Player {name} left the game!')
    else:
        await ctx.send("We couldn't remove you from the game!")

@botto.command(name='action', help='During game, sets actions to be done by the bot')
async def action(ctx:commands.Context, action:str, val=None):
    name = ctx.author.name
    if(game.started and game.playerExists(name)):
        await ctx.send(game.addAction(name, action, val))
        print(f'Action attempted by {name}: "{action}" (val = {val})')

botto.run(TOKEN)
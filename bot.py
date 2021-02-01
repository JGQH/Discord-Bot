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
    await ctx.send('''Welcome to "BattleBot"! A simple bot that let\'s you battle against a bunch of other people.

    Here are the game rules:
    -Each time a round starts, the position of everyone in the board is revealed to you.
    -Every round, you have the option to do a maximum of 3 actions:
        *move: Called using "!action move <dir>", were "dir" is either w, a, s, d. (No uppercase).
        *shoot: Called using "!action shoot". Your characters shoots using the rotation it currently has. If it impacts a player, that enemy loses 1hp.
        *aim: Called using "!action aim <deg>", were "deg" is the angle (In degrees) where your aiming to (Only integer values).
    -The actions mentioned are in order of priority, meaning that among the first actions realized by every player, the "move" actions will be done firts, followed by "shoot" actions and finally "aim" actions. -This behavior is repeated for every second and every third action in every round.
    -Invalid actions are not considered, but valid actions that contain invalid values will be considered (For example, calling "!action move t" will result in no movement).
    -Your character is the brightest circle in the grid, the rest are the enemies.
    -Edges of the grid are connected, meaning that crossing the left edge takes you to the right edge. This behavior works with the top edge and bottom edge too (This does not affect the \'bullets\' shot using "shoot" actions).
    -Each player has 3hp that represents your life points. Once they get to 0, you\'re out of the game.

    I hope it\'s all clear, and if it is, just say "!join" and wait for the game to begin!
''')
    pass

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
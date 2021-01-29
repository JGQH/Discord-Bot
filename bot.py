import os
from dotenv import load_dotenv
from discord.ext import commands
from game import Game

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

botto = commands.Bot(command_prefix='!')

game = Game()

#Events
@botto.event
async def on_ready():
    print(f'{botto.user.name} is alive!')

@botto.command(name='join_game', help='Allows a new player to join the current game')
async def join_game(ctx:commands.Context):
    if(game.addPlayer(ctx)):
        name = ctx.author.name
        print(f'Player {name} joined the game!')
        await ctx.send(f'Welcome aboard, {name}!')
    else:
        await ctx.send("We couldn't add you to the game!")

@botto.command(name='leave_game', help='Removes player from game if it hasn\'t started yet')
async def leave_game(ctx:commands.Context):
    name = ctx.author.name
    if(game.removePlayer(name)):
        print(f'Player {name} left the game!')
        await ctx.send(f'Until next time, {name}!')
    else:
        await ctx.send("We couldn't remove you from the game!")

botto.run(TOKEN)
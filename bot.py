import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

botto = commands.Bot(command_prefix='!')

#Events
@botto.event
async def on_ready():
    print(f'{botto.user.name} is alive!')

@botto.command(name='join_game', help='Allows a new player to join the current game')
async def join_game(ctx:commands.Context):
    name = ctx.author.name
    
    print(f'Player {name}')
    await ctx.send(f'Welcome, {name}!'), 

botto.run(TOKEN)
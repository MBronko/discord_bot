import discord
from discord.ext import commands
import random
import asyncio

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def eluwa(ctx):
    await ctx.send('no siemano')

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.command()
async def repeat(ctx, content, times: int, ):
    """Repeats a message multiple times."""
    print("{} powtarza {} - {} razy".format(ctx.author, content, times))
    for i in range(times):
        await ctx.send(content)

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))


# @bot.command()
# async def kick(ctx, person):

@bot.command()
async def changepref(ctx, prefix):
    bot.command_prefix = prefix

@bot.command()
async def dele(ctx, times):
    try:
        limit = int(times)+1 if int(times) <= 100 else 100
        await ctx.send("bedzie usuwanko", delete_after=1)
        await asyncio.sleep(1)
        await ctx.channel.purge(limit=limit)
    except ValueError:
        await ctx.send("liczbami upośledziu", delete_after=2)

bot.run('NjY1MTQzODA0MzczNzYyMDc4.Xp7ULQ.yCt9u9jOzQRRZ6gZOLBCpt1dPIs')
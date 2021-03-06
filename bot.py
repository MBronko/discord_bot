from manage_db import query_insert, create_db
from functions import get_prefix
from discord.ext import commands
import discord
import asyncio
import random

create_db()
token = open('token.txt').readline().strip('\n')
# 328935623144636426 mlp id

initial_extensions = [
    'cogs.lol',
    'cogs.main',
    'cogs.settings',
    'cogs.errorhandle',
    'cogs.cahgame'
]

description = 'No siemano tutej so komendy do bota i w ogóle, jeżeli zapomnisz prefixu to możesz też wywołać ' \
              'komende pingując bota'

owner_id = 322414584256266240

bot = commands.Bot(command_prefix=get_prefix, description=description, owner_id=owner_id)

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)


@bot.event
async def on_connect():
    await bot.change_presence(status=discord.Status.invisible)


@bot.event
async def on_ready():
    # game = discord.Game("gituwa elo")
    # await bot.change_presence(activity=game)
    print('Logged in as {}\n{}\n------'.format(bot.user.name, bot.user.id))


@bot.event
async def on_command(ctx):
    try:
        guild_name = ctx.guild.name
        channel_name = ctx.channel.name
    except AttributeError:
        guild_name = ""
        channel_name = ""
    inf = (guild_name, channel_name, ctx.author.name + "#" + str(ctx.author.discriminator), ctx.message.content)
    query_insert('INSERT INTO logs (server, channel, user, command, time) values (?, ?, ?, ?, current_timestamp)', inf)

bot.run(token)

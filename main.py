from dbwrapper import query_insert, create_db
from tools import get_prefix
from discord.ext import commands
from common import *
import discord

create_db()

bot = commands.Bot(command_prefix=get_prefix, description=DESCRIPTION, owner_id=OWNER_ID)

for extension in initial_extensions:
    bot.load_extension(extension)


@bot.event
async def on_ready():
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


bot.run(open('token.txt').readline().strip('\n'))

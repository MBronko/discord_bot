from discord.ext import commands
from manage_db import *

default_prefix = ''


def getprefix(bot, message):
    if message.guild is None:
        prefix = default_prefix
    else:
        server_id = message.guild.id
        try:
            prefix = query_select("SELECT info FROM rules WHERE server = ? AND type = 'prefix'", (server_id,))[0]
        except TypeError:
            prefix = default_prefix
    return commands.when_mentioned_or(prefix)(bot, message)

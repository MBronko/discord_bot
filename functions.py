from discord.ext import commands
from manage_db import query_select

default_prefix = ''


def get_prefix(bot, message):
    if message.guild is None:
        prefix = default_prefix
    else:
        server_id = message.guild.id
        try:
            prefix = query_select("SELECT value FROM rules WHERE server = ? AND type = 'prefix'", (server_id,))[0]
        except TypeError:
            prefix = default_prefix
    return commands.when_mentioned_or(prefix)(bot, message)


def try_convert(value, default=0, *types):
    if not types:
        types = (int,)
    for t in types:
        try:
            return t(value)
        except (ValueError, TypeError):
            continue
    return default

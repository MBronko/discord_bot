from discord.ext.commands import Bot
from utils.Common import DESCRIPTION, OWNER_ID
from utils.Tools import get_prefix, get_extensions
from os import environ

bot = Bot(command_prefix=get_prefix, description=DESCRIPTION, owner_id=OWNER_ID)

for extension in get_extensions():
    bot.load_extension(extension)

bot.run(environ['DISCORD_TOKEN'])

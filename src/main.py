from discord.ext.commands import Bot
from utils.Common import DESCRIPTION, OWNER_ID
from utils.Tools import get_prefix, get_extensions


bot = Bot(command_prefix=get_prefix, description=DESCRIPTION, owner_id=OWNER_ID)

for extension in get_extensions():
    bot.load_extension(extension)


token = open('../token.txt').readline().strip('\n')
bot.run(token)

from discord.ext.commands import Bot
from src.utils.common import DESCRIPTION, OWNER_ID
from utils.tools import get_prefix

bot = Bot(command_prefix=get_prefix, description=DESCRIPTION, owner_id=OWNER_ID)

initial_extensions = [
    # 'commands.lol',
    # 'commands.General',
    'src.commands.Settings',
    # 'commands.Voice',
    'src.commands.ErrorHandler',
    'src.commands.Events'
]

for extension in initial_extensions:
    bot.load_extension(extension)

token = open('../token.txt').readline().strip('\n')
bot.run(token)

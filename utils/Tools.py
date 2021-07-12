from discord.ext import commands
from utils.Models import Session, Rules
from utils.Common import DEFAULT_PREFIX, DEBUG
import os


def get_prefix(bot, message):
    if message.guild is None:
        prefix = DEFAULT_PREFIX
    else:
        with Session() as session:
            rule = session.query(Rules).where(Rules.server == message.guild.id, Rules.type == 'prefix').first()
            prefix = rule.value if rule else DEFAULT_PREFIX

    return commands.when_mentioned_or(prefix)(bot, message)


def get_extensions():
    ext = []
    for root, directories, files in os.walk('ext'):
        if DEBUG or 'debug' not in root:
            new_root = root.replace('/', '.')
            for file in files:
                if file.endswith('.py') and not file.startswith('Template'):
                    ext.append(f'{new_root}.{file[:-3]}')

    return ext

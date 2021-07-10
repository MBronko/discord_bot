from discord.ext import commands
from src.utils.models import Session, Rules
from src.utils.common import DEFAULT_PREFIX, DEBUG
import os


def get_prefix(bot, message, with_mention=True):
    if message.guild is None:
        prefix = DEFAULT_PREFIX
    else:
        with Session() as session:
            rule = session.query(Rules).where(Rules.server == message.guild.id, Rules.type == 'prefix').first()
            prefix = rule.value if rule else DEFAULT_PREFIX

    if with_mention:
        return commands.when_mentioned_or(prefix)(bot, message)
    else:
        return prefix


def get_extensions():
    ext = []
    for root, directories, files in os.walk('ext'):
        if DEBUG or 'debug' not in root:
            new_root = 'src.' + root.replace('/', '.')
            for file in files:
                if file.endswith('.py') and not file.startswith('Template'):
                    ext.append(f'{new_root}.{file[:-3]}')
    return ext
from discord.ext import commands
from utils.Models import Session, Rules
from utils.Common import DEFAULT_PREFIX, DEBUG
from discord.ext.commands.context import Context
from discord import Message, NotFound
from typing import Optional
import random
import os


def get_prefix(bot, message) -> list[str]:
    if message.guild is None:
        prefix = DEFAULT_PREFIX
    else:
        with Session() as session:
            rule = session.query(Rules).where(Rules.server == message.guild.id, Rules.type == 'prefix').first()
            prefix = rule.value if rule else DEFAULT_PREFIX

    return commands.when_mentioned_or(prefix)(bot, message)


def get_extensions() -> list[str]:
    ext = []
    for root, directories, files in os.walk('ext'):
        if (DEBUG or 'debug' not in root.lower()) and '__pycache__' not in root:
            new_root = root.replace(os.path.sep, '.')
            for file in files:
                if file.endswith('.py') and not file.startswith('Template'):
                    ext.append(f'{new_root}.{file[:-3]}')

    return ext


def random_color() -> int:
    return random.randint(0, 0xffffff)


async def fetch_message(ctx: Context, msg_id: int) -> Optional[Message]:
    try:
        return await ctx.fetch_message(msg_id)
    except NotFound:
        return None

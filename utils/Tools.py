from discord.ext.commands import Context, Bot
from discord.ext import commands
from discord import Message, NotFound

from utils.Models import Session, Rules
from utils.Common import DEFAULT_PREFIX, DEBUG
from leaguetools.RiotAPI.tasks import get_riot_api_status

from typing import Optional
import random
import os


def get_prefix(bot: Bot, message: Message) -> list[str]:
    if message.guild is None:
        prefix = DEFAULT_PREFIX
    else:
        with Session() as session:
            rule = session.query(Rules).where(Rules.server == message.guild.id, Rules.type == 'prefix').first()
            prefix = rule.value if rule else DEFAULT_PREFIX

    return commands.when_mentioned_or(prefix)(bot, message)


def get_extensions() -> list[str]:
    blacklisted_dirs = ['debug', '__pycache__']
    ext = []

    riot_api_active = bool(get_riot_api_status())

    for root, directories, files in os.walk('ext'):
        skip = any(ext_dir in root.lower() for ext_dir in blacklisted_dirs)

        if DEBUG or not skip:
            new_root = root.replace(os.path.sep, '.')
            for file in files:
                valid_file = file.endswith('.py') and not file.startswith('Template')
                valid_riot_api_key = riot_api_active or 'RiotAPI' not in file

                if valid_file and valid_riot_api_key:
                    ext.append(f'{new_root}.{file[:-3]}')

    return ext


def random_color() -> int:
    return random.randint(0, 0xffffff)


async def fetch_message(ctx: Context, msg_id: int) -> Optional[Message]:
    try:
        return await ctx.fetch_message(msg_id)
    except NotFound:
        return None

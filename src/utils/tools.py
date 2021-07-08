from discord.ext import commands
from src.utils.models import Session, Settings
from src.utils.common import DEFAULT_PREFIX


def get_prefix(bot, message):
    if message.guild is None:
        prefix = DEFAULT_PREFIX
    else:
        with Session() as session:
            rule = session.query(Settings).where(Settings.server == message.guild.id, Settings.type == "prefix").first()
            prefix = rule.value if rule else DEFAULT_PREFIX

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

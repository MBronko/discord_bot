from discord.ext.commands import Context
from pyot.models import lol
from pyot.core.exceptions import NotFound

from leaguetools.RiotAPI.tools import parse_possible_champion_keys
from utils.Models import Session, LeaguechampsKeyCache

from typing import Optional


async def get_specified_champion(ctx: Context, name: tuple[str], champ_func):
    possible_keys, parsedname = parse_possible_champion_keys(name)
    champ = None
    for key in possible_keys:
        try:
            champ = await champ_func(key=key).get()
            break
        except (NotFound, KeyError):
            try:
                champ = await champ_func(name=key).get()
                break
            except (NotFound, KeyError):
                pass

    if champ:
        with Session() as session:
            cache = session.query(LeaguechampsKeyCache).where(LeaguechampsKeyCache.parsedname == parsedname).first()
            if not cache:
                new_key = LeaguechampsKeyCache()
                new_key.key = champ.key
                new_key.parsedname = parsedname
                session.add(new_key)
                session.commit()
    else:
        await ctx.send('Champion not found')

    return champ


async def get_champion(ctx: Context, name: tuple[str]) -> Optional[lol.Champion]:
    return await get_specified_champion(ctx, name, lol.Champion)


async def get_meraki_champion(ctx: Context, name: tuple[str]) -> Optional[lol.MerakiChampion]:
    return await get_specified_champion(ctx, name, lol.MerakiChampion)


async def get_summoner(ctx: Context, name: str) -> Optional[lol.Summoner]:
    if name:
        try:
            return await lol.Summoner(name=name).get()
        except NotFound:
            pass
    await ctx.send('Summoner not found')
    return None

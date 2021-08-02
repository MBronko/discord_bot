from pyot.models import lol
from pyot.core.exceptions import NotFound
from leaguetools.RiotAPI.tools import parse_possible_champion_keys
from utils.Models import Session, LeaguechampsKeyCache
from typing import Optional


async def get_specified_champion(name: tuple[str], champ_func):
    possible_keys, parsedname = parse_possible_champion_keys(name)
    champ = None
    print(possible_keys)
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

    return champ


async def get_champion(name: tuple[str]) -> Optional[lol.Champion]:
    return await get_specified_champion(name, lol.Champion)


async def get_meraki_champion(name: tuple[str]) -> Optional[lol.MerakiChampion]:
    return await get_specified_champion(name, lol.MerakiChampion)


async def get_summoner(name: str) -> Optional[lol.Summoner]:
    if name:
        try:
            summoner = await lol.Summoner(name=name).get()
            return summoner
        except NotFound:
            pass
    return None


async def summoner_level(name):
    '''Get summoner level by name and platform'''

    # Pyot Model: lol
    # Pyot Core Object: Summoner
    # Refer: https://paaksing.github.io/Pyot/models/lol_summoner.html

    try:
        summoner = await lol.Summoner(name=name).get()
        print(summoner.name, 'in', summoner.platform.upper(), 'is level', summoner.level)
    except NotFound:
        print('Summoner not found')

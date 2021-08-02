from pyot.models import lol
from pyot.core.exceptions import NotFound
from typing import Optional


async def get_summoner(name: str) -> Optional[lol.Summoner]:
    try:
        summoner = await lol.Summoner(name=name).get()
        return summoner
    except NotFound:
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

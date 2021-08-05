# Default settings for pyot projects.
# Change these settings according to your needs.

import platform
from os import environ
from utils.Common import DEBUG

# Fix: Windows `asyncio.run()` will throw `RuntimeError: Event loop is closed`.
# Refer: https://github.com/aio-libs/aiohttp/issues/4324

if platform.system() == 'Windows':
    from pyot.utils.internal import silence_proactor_pipe_deallocation

    silence_proactor_pipe_deallocation()

# Pyot documentations for settings
# https://paaksing.github.io/Pyot/core/settings.html

# Pyot documentations for pipeline stores
# https://paaksing.github.io/Pyot/stores/

from pyot.core import Settings

#  Settings here
default_exp_time = 300  # default cache expiration in seconds

default_exp_time_endpoints = [
    'summoner_v4_by_name',
    'summoner_v4_by_id',
    'champion_mastery_v4_by_champion_id',
    'clash_v1_players',
    'clash_v1_teams',
    'match_v4_matchlist',
]

additional_expirations = {
    # 'endpoint': 5
}
#  end of settings

log_level = 30 if DEBUG else 0

expirations = dict({key: default_exp_time for key in default_exp_time_endpoints}, **additional_expirations)

Settings(
    MODEL='LOL',
    DEFAULT_PLATFORM=environ['DEFAULT_PLATFORM'],
    DEFAULT_REGION=environ['DEFAULT_REGION'],
    DEFAULT_LOCALE=environ['DEFAULT_LOCALE'],
    PIPELINE=[
        {
            'BACKEND': 'pyot.stores.Omnistone',
            'LOG_LEVEL': log_level,
            'EXPIRATIONS': expirations
        },
        {
            'BACKEND': 'pyot.stores.MerakiCDN',
            'LOG_LEVEL': log_level
        },
        {
            'BACKEND': 'pyot.stores.CDragon',
            'LOG_LEVEL': log_level
        },
        {
            'BACKEND': 'pyot.stores.RiotAPI',
            'LOG_LEVEL': log_level,
            'API_KEY': environ['RIOT_API_KEY']  # API KEY
        }
    ]
).activate()  # <- DON'T FORGET TO ACTIVATE THE SETTINGS

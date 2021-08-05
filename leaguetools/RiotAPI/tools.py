from pyot.models import lol
from pyot.utils import PtrCache
from discord import Embed
from urllib import parse

from leaguetools.ChampRollTools import parse_champion_name
from leaguetools.Constants import lane_data
from utils.Models import Session, Leaguechamps, LeaguechampsKeyCache
from utils.Common import EMBED_EMPTY_VAL


def parse_possible_champion_keys(name: tuple[str]) -> tuple[set[str], str]:
    parsed = [x.capitalize() for segment in name if segment != '\'' for x in segment.split('\'')]

    res = set()

    if not parsed:
        return res, ''

    capitalized_segments = ''.join(parsed)
    capitalized = capitalized_segments.capitalize()

    with Session() as session:
        parsedname = parse_champion_name(capitalized)

        champ = session.query(LeaguechampsKeyCache).where(LeaguechampsKeyCache.parsedname == parsedname).first()
        if champ:
            res.add(champ.key)

        res.update([capitalized, capitalized_segments])

        champ = session.query(Leaguechamps).where(Leaguechamps.parsedname == parsedname).first()
        if champ:
            res.add(champ.name)

    return res, parsedname


def match_history_most_played_champs(history: lol.MatchHistory) -> list[int, int]:
    results = {}
    for entry in history.entries:
        champ = entry.champion_id
        if champ in results:
            results[champ] += 1
        else:
            results[champ] = 1

    return sorted(results.items(), key=lambda item: item[1], reverse=True)


def match_history_lanes_counter(history: lol.MatchHistory) -> dict[str, int]:
    results = {}
    for key in list(lane_data.keys())[:5]:
        results[key] = 0

    for entry in history.entries:
        lane = entry.lane  # TOP,JUNGLE,MID,BOTTOM,NONE
        role = entry.role  # SOLO,DUO,DUO_SUPPORT,DUO_CARRY,NONE

        if lane == 'MID':
            lane = 'MIDDLE'

        if lane in ['TOP', 'JUNGLE', 'MIDDLE']:
            results[lane] += 1
        elif lane != 'NONE' and role in ['DUO_SUPPORT', 'DUO_CARRY']:
            bottom_lanes = {'DUO_SUPPORT': 'UTILITY', 'DUO_CARRY': 'BOTTOM'}
            results[bottom_lanes[role]] += 1

    return results


def match_history_stats(history: lol.MatchHistory) -> dict:
    pass  # todo get stats like winrate


async def gather_summoner_data(summoner: lol.Summoner, position: str, match_history: lol.MatchHistory, top_champions: list[tuple[str, int]]) -> Embed:
    embed = Embed()
    embed.set_author(name=summoner.name, icon_url=lane_data[position]['icon_url'])

    icon = await summoner.profile_icon.get()  # get from cache
    embed.set_thumbnail(url=icon.icon_abspath)

    parsed_name = parse.quote(summoner.name)
    op_gg_url = f'[op.gg](https://eune.op.gg/summoner/userName={parsed_name})'

    embed.add_field(name=EMBED_EMPTY_VAL, value=f'level: {summoner.level}', inline=False)

    champions_info = [f'{champ}: {n}' for champ, n in top_champions]
    embed.add_field(name='Top 5 clash champions', value='\n'.join(champions_info), inline=False)

    lanes_counter = match_history_lanes_counter(match_history)
    lanes_info = [f'{lane_data[lane]["display_name"]}: {n}' for lane, n in lanes_counter.items()]

    embed.add_field(name='Clash positions played', value='\n'.join(lanes_info), inline=False)

    embed.add_field(name=EMBED_EMPTY_VAL, value=op_gg_url, inline=False)

    return embed


def refresh_op_gg_profiles(names: list[str]) -> None:
    pass  # todo refresh op gg profile

from discord import Embed
from discord.ext.commands import Context

from utils.Models import Session, Rules, Leaguechamps
from utils.Queries import get_champ_by_name, get_champs_by_lane, get_champs_by_lane_not_in_list
from utils.Common import EMBED_EMPTY_VAL
from leaguetools.Constants import lane_info
from leaguetools.WebScrapingParsers import parse_lolwiki, parse_gg

from datetime import datetime, timedelta
from sqlalchemy import func
from bs4 import BeautifulSoup
from typing import Optional
import requests

icon_url_prefix = 'https://vignette.wikia.nocookie.net/leagueoflegends/images/'
team_icon_url = 'https://static.wikia.nocookie.net/leagueoflegends/images/8/80/Summoner%27s_Rift_icon.png'

hours_cd = 12
minutes_cd = 0
seconds_cd = 0

db_identifier = 'lolchamps'

wiki_url = 'https://leagueoflegends.fandom.com/wiki/List_of_champions_by_draft_position'
gg_url = 'https://champion.gg/statistics/?league=plat'

fetch_data = [[wiki_url, parse_lolwiki], [gg_url, parse_gg]]


async def request_and_parse(ctx: Context, url: str, callback) -> Optional[dict]:
    res = requests.get(url)
    if res.status_code == 200:
        return await callback(BeautifulSoup(res.text, 'html.parser'))
    await ctx.send(f'Fail: <{url}> returned code {res.status_code}')
    return None


async def update_database(champions: dict) -> None:
    if champions:
        bulk_save = []
        with Session() as session:
            for champion in champions:
                db_champ = get_champ_by_name(session, champion['name'])
                if not db_champ:
                    db_champ = Leaguechamps()
                    db_champ.name = champion['name']
                    bulk_save.append(db_champ)

                db_champ.top = db_champ.top or champion['top']
                db_champ.jungle = db_champ.jungle or champion['jungle']
                db_champ.mid = db_champ.mid or champion['mid']
                db_champ.adc = db_champ.adc or champion['adc']
                db_champ.support = db_champ.support or champion['support']

            session.bulk_save_objects(bulk_save)
            session.commit()


async def fetch_champions(ctx: Context) -> bool:
    print('fetching champions')

    update = False
    parsed = []

    for link, callback in fetch_data:
        res = await request_and_parse(ctx, link, callback)
        update = update or bool(res)
        parsed.append(res)

    if update:
        with Session() as session:
            session.query(Leaguechamps).delete()

            rule = session.query(Rules).where(Rules.type == db_identifier).first()
            if rule:
                rule.timestamp = func.now()
            else:
                rule = Rules()
                rule.type = db_identifier
                session.add(rule)
            session.commit()

        for data in parsed:
            await update_database(data)

        return True
    return False


async def display_champions(ctx: Context, times: int, lane: str, color: int):
    # check if update is needed
    with Session() as session:
        last_time = datetime.utcnow() - timedelta(hours=hours_cd, minutes=minutes_cd, seconds=seconds_cd)
        res = session.query(Rules).where(Rules.type == db_identifier, Rules.timestamp > last_time).first()
        if not res:
            await fetch_champions(ctx)

    if times < 1:
        times = 1

    embed = Embed(color=color)
    if lane == 'team':
        used_champs = []
        embed.set_author(name=lane.capitalize(), icon_url=team_icon_url)
        for lane in lane_info.keys():
            column = lane_info[lane]['db_field']
            with Session() as session:
                champ_list = get_champs_by_lane_not_in_list(session, column, used_champs, times)
            champ_names = [champ.name for champ in champ_list]
            used_champs += champ_names
            embed.add_field(name=lane.capitalize(), value='/\u200b'.join(champ_names), inline=False)
    else:
        column = lane_info[lane]['db_field']
        with Session() as session:
            champ_list = get_champs_by_lane(session, column, times)
        name_list = [champ.name for champ in champ_list]

        embed.set_author(name=lane.capitalize(), icon_url=icon_url_prefix + lane_info[lane]['icon_name'])
        embed.add_field(name=EMBED_EMPTY_VAL, value='\n'.join(name_list))
    await ctx.send(embed=embed)

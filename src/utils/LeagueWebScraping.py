# from discord import Embed
# from sqlalchemy import func
from src.utils.Models import Session, Rules, Leaguechamps
from sqlalchemy import func
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
# import json
import re
import requests

wiki_url = 'https://leagueoflegends.fandom.com/wiki/List_of_champions_by_draft_position'
gg_url = 'https://champion.gg/statistics/?league=plat'

icon_url_prefix = 'https://vignette.wikia.nocookie.net/leagueoflegends/images/'
icon_url_dict = {
    'top': 'e/ef/Top_icon.png',
    'jungle': '1/1b/Jungle_icon.png',
    'middle': '9/98/Middle_icon.png',
    'adc': '9/97/Bottom_icon.png',
    'support': 'e/e0/Support_icon.png'
}
lanes = [
    'top',
    'jungle',
    'mid',
    'adc',
    'support'
]
team_icon_url = 'https://cdn.discordapp.com/attachments/702124910981415005/704348781965213746/gotawamapa.png'

hours_cd = 0
minutes_cd = 0
seconds_cd = 5

db_identifier = 'lolchamps'


async def parse_lolwiki(html):
    result = []
    table = html.find("table", class_="article-table sortable")  # table with all champions

    for row in table.find_all('tr')[1:]:  # iterate over all positions in table
        champ_data = {'name': row.find('td').text.strip()}

        for idx, td in enumerate(row.find_all('td')[1:-1]):
            champ_data[lanes[idx]] = bool(td.find_all())  # or td.text.strip() != '' # to include op.gg suggestions
        result.append(champ_data)
    return [{'name': 'test', 'top': False, 'jungle': False, 'mid': True, 'adc': True, 'support': True}]
    # return result


async def parse_gg(html):
    table_class = 'Champions__TableWrapper-rli9op-0 AllChampionsTable__TableContentWrapper-cpgif4-0 jlzfMF'
    div = html.find('div', class_=table_class).find_all('div', recursive=False)[1].find().find()
    rows = div.find_all('div', recursive=False)

    buffer = {}
    for row in rows:
        name = row.find('span', class_='champion-name').text

        if name not in buffer:
            buffer[name] = {'name': name, 'top': False, 'jungle': False, 'mid': False, 'adc': False, 'support': False}

        href = row.find('a', class_='champion-tier-container')['href']
        lane = href.split('/')[-1].lower()
        lane = lane if lane != 'middle' else 'mid'

        buffer[name][lane] = True
    return buffer.values()


fetch_data = [[wiki_url, parse_lolwiki], [gg_url, parse_gg]]


async def request_and_parse(ctx, url, callback):
    res = requests.get(url)
    if res.status_code == 200:
        return await callback(BeautifulSoup(res.text, 'html.parser'))
    await ctx.send(f'Fail: <{url}> returned code {res.status_code}')
    return False


async def update_database(champions):
    if champions:
        for champion in champions:
            with Session() as session:
                db_champ = session.query(Leaguechamps).where(Leaguechamps.name == champion['name']).first()
                if not db_champ:
                    db_champ = Leaguechamps()
                    db_champ.name = champion['name']
                    session.add(db_champ)

                db_champ.top = db_champ.top or champion['top']
                db_champ.jungle = db_champ.jungle or champion['jungle']
                db_champ.mid = db_champ.mid or champion['mid']
                db_champ.adc = db_champ.adc or champion['adc']
                db_champ.support = db_champ.support or champion['support']

                session.commit()


async def fetch_champions(ctx):
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


async def display_champions(ctx, lane, times, color):
    # check if update is needed
    with Session() as session:
        last_time = datetime.utcnow() - timedelta(hours=hours_cd, minutes=minutes_cd, seconds=seconds_cd)
        res = session.query(Rules).where(Rules.type == db_identifier, Rules.timestamp > last_time).first()
        if not res:
            await fetch_champions(ctx)

    await ctx.send('tu championy beda')

    # TODO display champions for lane
#     embed = Embed(color=color)
#     if lane != 'team':
#         champ_list = query_selectall('SELECT champ FROM lolchamps '
#                                      'WHERE %s = ''"tak" ORDER BY RANDOM() LIMIT ?' % lane, (times,), True)
#         embed.set_author(name=lane.capitalize(), icon_url=icon_url_prefix + icon_url_dict[lane])
#         embed.add_field(name='\u200b', value='\n'.join(champ_list))
#     else:
#         lanes = ['top', 'jungle', 'middle', 'adc', 'support']
#         used_champs = []
#         embed.set_author(name=lane.capitalize(), icon_url=team_icon_url)
#         for lane in lanes:
#             args = used_champs + list((times,))
#             sql = 'SELECT champ FROM lolchamps WHERE %s="tak" ' \
#                   'AND champ not in (%s) ORDER BY RANDOM() LIMIT ?' % (lane, ','.join(['?'] * len(used_champs)))
#             champ_list = query_selectall(sql, args, True)
#             used_champs += champ_list
#             embed.add_field(name=lane.capitalize(), value='/\u200b'.join(champ_list), inline=False)
#     await ctx.send(embed=embed)

# from discord import Embed
# from sqlalchemy import func
from src.utils.Models import Session, Rules, Leaguechamps
# from bs4 import BeautifulSoup
# import json
# import re
import requests

wiki_url = 'https://leagueoflegends.fandom.com/wiki/List_of_champions/Position'
gg_url = 'https://champion.gg/statistics/?league=plat'

fetch_urls = [wiki_url, gg_url]

icon_url_prefix = 'https://vignette.wikia.nocookie.net/leagueoflegends/images/'
icon_url_dict = {
    'top': 'e/ef/Top_icon.png',
    'jungle': '1/1b/Jungle_icon.png',
    'middle': '9/98/Middle_icon.png',
    'adc': '9/97/Bottom_icon.png',
    'support': 'e/e0/Support_icon.png'
}
team_icon_url = 'https://cdn.discordapp.com/attachments/702124910981415005/704348781965213746/gotawamapa.png'


async def parse_lolwiki(http):
    return http


async def parse_champion_gg(http):
    return http


async def requests_get(ctx, url, callback):
    res = requests.get(url)
    if res.status_code == 200:
        return await callback(res.text)
    await ctx.send(f'fail: <{url}> returned code {res.status_code}')
    return False


async def update_database(champions):
    pass


async def fetch_champions(ctx):
    print('fetching champions')

    res1 = await requests_get(ctx, wiki_url, parse_lolwiki)
    await update_database(res1)

    res2 = await requests_get(ctx, gg_url, parse_champion_gg)
    await update_database(res2)

    return res1 or res2


async def display_champions(ctx, lane, times, color):
    with Session() as session:
        res = session.query(Rules).where(Rules.type == 'lolchamps').first()
        if not res:
            await fetch_champions(ctx)


# async def fetch_champions(ctx, times, lane, color):
#     if not query_select('SELECT * from rules where type="lolchamps" and '
#                         '(strftime("%s",current_timestamp)-strftime("%s",value)<60*60*24*7)'):
#         print('pobieranie bazy danych')
#         query_insert('DELETE FROM rules where type="lolchamps"')
#         query_insert('DELETE FROM "lolchamps"')
#         query_insert('INSERT INTO rules (type, value) values ("lolchamps", current_timestamp)')
#
#         html = BeautifulSoup(await simple_get(wiki_url), 'html.parser')
#         the_table = html.find("table", class_="article-table sortable")
#         total = []
#         for row in the_table.find_all('tr')[1:]:
#             tmp_list = [(row.find_all('td')[0].text.strip())]
#             for td in row.find_all('td')[1:-1]:
#                 if td.find_all() or td.text.strip() != '':
#                     tmp_list.append("tak")
#                 else:
#                     tmp_list.append("nie")
#             total.append(tmp_list)
#         query_insertmany('INSERT INTO lolchamps (champ,top,jungle,middle,adc,support) values (?,?,?,?,?,?)', total)
#
#         html = BeautifulSoup(await simple_get(gg_url), 'html.parser')
#         json_data = html.find("script", text=re.compile('matchupData.stats'))
#         data = json.loads(json_data.string.replace('matchupData.stats = ', '').strip('')[:-2])
#
#         for champ in data:
#             query_insert('UPDATE lolchamps SET %s = "tak" WHERE champ = ?' % champ['role'].lower(), (champ['title'],))
#
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

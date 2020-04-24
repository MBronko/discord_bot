from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from manage_db import *
import random
import json
import re

wiki_url = 'https://leagueoflegends.fandom.com/wiki/List_of_champions/Position'
gg_url = 'https://champion.gg/statistics/'


def log_error(e):
    print(e)


def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


async def fetch_champions(ctx, times, lane='team'):
    if not query_select('SELECT * from rules where type="lolchamps" and '
                        '(strftime("%s",current_timestamp)-strftime("%s",info)<60*60*24*7)'):
        print('pobieranie bazy danych')
        query_insert('DELETE FROM rules where type="lolchamps"')
        query_insert('DELETE FROM "lolchamps"')
        query_insert('INSERT INTO rules (type, info) values ("lolchamps", current_timestamp)')

        html = BeautifulSoup(simple_get(wiki_url), 'html.parser')
        the_table = html.find("table", class_="article-table sortable")
        total = []
        for row in the_table.find_all('tr')[1:]:
            tmp_list = [(row.find_all('td')[0].text.strip())]
            for td in row.find_all('td')[1:-1]:
                if td.find_all() or td.text.strip() != '':
                    tmp_list.append("tak")
                else:
                    tmp_list.append("nie")
            total.append(tmp_list)
        query_insertmany('INSERT INTO lolchamps (champ,top,jungle,middle,adc,support) values (?,?,?,?,?,?)', total)

        html = BeautifulSoup(simple_get(gg_url), 'html.parser')
        json_data = html.find("script", text=re.compile('matchupData.stats'))
        data = json.loads(json_data.string.replace('matchupData.stats = ', '').strip('')[:-2])

        for champ in data:
            query_insert('UPDATE lolchamps SET %s = "tak" WHERE champ = ?' % champ['role'].lower(), (champ['title'],))
    try:
        times = int(times) if int(times) > 0 and times != '' else 1
    except Exception:
        times = 1
    if lane != 'team':
        r = query_selectall('SELECT champ FROM lolchamps WHERE %s = ''"tak" ORDER BY RANDOM() LIMIT ?' % lane, (times,))
        champ_list = map(lambda x: x[0], r)
        await ctx.send('```{}```'.format("/".join(champ_list)))
    else:
        lanes = ['top', 'jungle', 'middle', 'adc', 'support']
        team_champs = []
        for lane in lanes:
            r = query_selectall('SELECT champ FROM lolchamps WHERE %s="tak" ORDER BY RANDOM() LIMIT ?' % lane, (times,))
            champ_list = map(lambda x: x[0], r)
            team_champs.append(lane.capitalize() + ": " + "/".join(champ_list))
        await ctx.send('```{}```'.format("\n".join(team_champs)))

import discord
from discord.ext import commands
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import random
import sqlite3
import json
import re

wiki_url = 'https://leagueoflegends.fandom.com/wiki/List_of_champions/Position'
gg_url = 'https://champion.gg/statistics/'

db_name = 'botdb.db'
conn = sqlite3.connect(db_name)
cur = conn.cursor()

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
    cur.execute('SELECT * from rules where type="lolchamps" and '
                '(strftime("%s",current_timestamp)-strftime("%s",info)>60*60*24*7)')
    if cur.fetchone():
        cur.execute('DELETE FROM rules where type="lolchamps"')
        cur.execute('DELETE FROM "lolchamps"')
        cur.execute('INSERT INTO rules (type, info) values ("lolchamps", current_timestamp)')

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
        cur.executemany('INSERT INTO lolchamps (champ, top, jungle, middle, adc, support) values (?,?,?,?,?,?)', total)
        html = BeautifulSoup(simple_get(gg_url), 'html.parser')
        json_data = html.find("script", text=re.compile('matchupData.stats'))
        data = json.loads(json_data.string.replace('matchupData.stats = ', '').strip('')[:-2])

        for champ in data:
            cur.execute('UPDATE lolchamps SET %s = "tak" WHERE champ = ?' % champ['role'].lower(), (champ['title'],))
        conn.commit()

    try:
        times = int(times) if int(times) > 0 and times != '' else 1
    except Exception:
        times = 1
    if lane != 'team':
        cur.execute('SELECT champ FROM lolchamps WHERE %s = "tak" ORDER BY RANDOM() LIMIT ?' % lane, (times,))
        await ctx.send('```{}```'.format("/".join(map(lambda x: x[0], cur.fetchall()))))
    else:
        lanes = ['top', 'jungle', 'middle', 'adc', 'support']
        team_champs = []
        for lane in lanes:
            cur.execute('SELECT champ FROM lolchamps WHERE %s = "tak" ORDER BY RANDOM() LIMIT ?' % lane, (times,))
            team_champs.append(lane.capitalize() + ": " + "/".join(map(lambda x: x[0], cur.fetchall())))
        await ctx.send('```{}```'.format("\n".join(team_champs)))


class LolCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=('toplane',))
    async def top(self, ctx, times=''):
        await fetch_champions(ctx, times, "top")

    @commands.command(aliases=('jgl',))
    async def jungle(self, ctx, times=''):
        await fetch_champions(ctx, times, "jungle")

    @commands.command(aliases=('middle', 'midlane'))
    async def mid(self, ctx, times=''):
        await fetch_champions(ctx, times, "middle")

    @commands.command()
    async def adc(self, ctx, times=''):
        await fetch_champions(ctx, times, "adc")

    @commands.command(aliases=('support',))
    async def supp(self, ctx, times=''):
        await fetch_champions(ctx, times, "support")

    @commands.command()
    async def team(self, ctx, times=''):
        await fetch_champions(ctx, times)

    @commands.command()
    async def tft(self, ctx, times=''):
        try:
            times = int(times) if 20 >= int(times) > 0 and times != '' else 2
        except Exception:
            times = 2
        types = ['Infiltrator', 'Sorcerer', 'Blademaster', 'Brawler', 'Mystic', 'Protector', 'Sniper', 'Blaster',
                 'Demolitionist', 'Mana-Reaver', 'Vanguard', 'Dark Star', 'Mech Pilot', 'Cybernetic', 'Star Guardian',
                 'Chrono', 'Celestial', 'Space Pirate', 'Void', 'Rebel']
        random.shuffle(types)
        msg = []
        for _ in range(times):
            msg.append(types.pop())
        await ctx.send(' i '.join(msg))


def setup(bot):
    bot.add_cog(LolCog(bot))

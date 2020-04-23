import discord
from discord.ext import commands
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import random

wiki_url = 'https://leagueoflegends.fandom.com/wiki/List_of_champions/Position'


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


def get_champions_list():
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
    return total


def get_champions_by_lane(lane):
    champs = []
    for champ in get_champions_list():
        if champ[lane] == 'tak':
            champs.append(champ[0])
    random.shuffle(champs)
    return champs


async def return_champ(ctx, times, lane):
    champs = get_champions_by_lane(lane)
    try:
        times = int(times) if len(champs) >= int(times) > 0 and times != '' else 1
    except Exception:
        times = 1
    msg = ''
    for _ in range(times):
        msg += '/' + champs.pop()
    await ctx.send("```{}```".format(msg[1:]))


class LolCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def top(self, ctx, times=''):
        await return_champ(ctx, times, 1)

    @commands.command()
    async def jungle(self, ctx, times=''):
        await return_champ(ctx, times, 2)

    @commands.command()
    async def mid(self, ctx, times=''):
        await return_champ(ctx, times, 3)

    @commands.command()
    async def adc(self, ctx, times=''):
        await return_champ(ctx, times, 4)

    @commands.command()
    async def supp(self, ctx, times=''):
        await return_champ(ctx, times, 5)

    @commands.command()
    async def team(self, ctx):
        champs = []
        used = []
        champion_list = get_champions_list()
        random.shuffle(champion_list)
        lanes = ['Top', 'Jungle', 'Mid', 'Adc', 'Supp']
        for x in range(1, 6):
            for champ in champion_list:
                if champ[x] == 'tak' and not champ[0] in used:
                    champs.append('{}: {}'.format(lanes[x-1], champ[0]))
                    used.append(champ[0])
                    break
        await ctx.send("```{}```".format('\n'.join(champs)))

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
        msg = ''
        for _ in range(times):
            msg += 'i ' + types.pop() + ' '
        await ctx.send(msg[2:])


def setup(bot):
    bot.add_cog(LolCog(bot))

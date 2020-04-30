import asyncio
import discord
from discord.ext import commands
import typing
import aiohttp
from bs4 import BeautifulSoup
import json
from manage_db import query_select, query_insert
from urllib.request import Request, urlopen
from urllib.error import *
import html


async def simple_get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            data = await r.text()
            if r.status == 200 and data:
                return json.loads(data)


async def get_deck(ctx, deck_id):
    url = 'https://api.cardcastgame.com/v1/decks/%s/cards' % deck_id
    json_data = await simple_get(url)
    if not json_data:
        return await ctx.send('Nie mogę znaleźć decku')
    result = {}
    card_types = ['responses', 'calls']
    for card_type in card_types:
        result[card_type] = list(map(lambda x: x['text'], json_data[card_type]))
    # print(result['responses'][0][0])
    return result


async def get_deckinfo(ctx, deck_id):
    url = 'https://api.cardcastgame.com/v1/decks/%s' % deck_id
    json_data = await simple_get(url)
    if not json_data:
        return await ctx.send(f'Nie mogę znaleźć decku {deck_id}')
    # print(json_data['name'], json_data['description'], json_data['call_count'], json_data['response_count'])
    return json_data


async def get_summed_decks(ctx):
    decks_id = query_select('SELECT value FROM cahgame WHERE server=? AND type="saved_decks"'
                            , (ctx.guild.id,))
    # decks_id = ('V7MTP', 'W72H4', 'W72H4', 'W72H4', 'W72H4')
    if not decks_id:
        return await ctx.send('Nie masz zapisanych żadnych decków')
    print(decks_id[0])
    card_types = ['responses', 'calls']
    total_deck = {'calls': [], 'responses': []}
    for deck_id in decks_id[0].split(' '):
        deck = await get_deck(ctx, deck_id)
        for card_type in card_types:
            total_deck[card_type] += deck[card_type]
    return total_deck


class CardsAgainstHumanity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def addcardcast(self, ctx, *, decks: str):
        added_before = query_select('SELECT value FROM cahgame WHERE server=? AND type="saved_decks"'
                                    , (ctx.guild.id,))
        to_save = []
        if added_before:
            to_save = added_before[0].split(' ')
        query_insert('DELETE FROM cahgame WHERE server=? AND type="saved_decks"', (ctx.guild.id,))
        for deck in decks.split(' '):
            deck_info = await get_deckinfo(ctx, deck)
            if isinstance(deck_info, dict):
                if deck not in to_save:
                    to_save.append(deck)
                await ctx.send(f'Dodano {deck_info["name"]} do zapisanych decków')
        if to_save:
            query_insert('INSERT INTO cahgame (server, value, type) values (?, ?, "saved_decks")',
                         (ctx.guild.id, " ".join(to_save)))
        else:
            await ctx.send('Żaden z decków nie zadziałał')

    @commands.command()
    async def cahstart(self, ctx):
        deck = await get_summed_decks(ctx)
        if not isinstance(deck, dict):
            return
        print(deck)

def setup(bot):
    bot.add_cog(CardsAgainstHumanity(bot))



# info_json = get_json(info_url)
# print('deck:', info_json['name'], 'desc:', info_json['description'], 'calls:', info_json['call_count'], 'responses:'
#       , info_json['response_count'])

# deck_json = get_json(deck_url)
# print(list(map(lambda x: x['text'], deck_json['responses'])))
# print(list(map(lambda x: x['text'], deck_json['calls'])))




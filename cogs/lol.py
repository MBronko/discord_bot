from discord.ext import commands
from discord.ext.commands import command
import random
from cogs.webscraping import fetch_champions
from manage_db import query_insert
from functions import try_convert


class LeagueOfLegends(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(aliases=('toplane',))
    async def top(self, ctx, times=''):
        """Wylosuj sobie topa"""
        await fetch_champions(ctx, try_convert(times, 1), "top")

    @command(aliases=('jgl',))
    async def jungle(self, ctx, times=''):
        """Wylosuj sobie jungle"""
        await fetch_champions(ctx, try_convert(times, 1), "jungle")

    @command(aliases=('middle', 'midlane'))
    async def mid(self, ctx, times=''):
        """Wylosuj sobie mida"""
        await fetch_champions(ctx, try_convert(times, 1), "middle")

    @command()
    async def adc(self, ctx, times=''):
        """Wylosuj sobie adc"""
        await fetch_champions(ctx, try_convert(times, 1), "adc")

    @command(aliases=('support',))
    async def supp(self, ctx, times=''):
        """Wylosuj sobie suppa"""
        await fetch_champions(ctx, try_convert(times, 1), "support")

    @command()
    async def team(self, ctx, times=''):
        """Wylosuj sobie cały team"""
        await fetch_champions(ctx, try_convert(times, 1))

    @command()
    async def resetdb(self, ctx):
        """Zaktualizuj bazę danych z champion.gg i lolwiki"""
        query_insert('DELETE FROM lolchamps')
        query_insert('DELETE FROM rules where type="lolchamps"')
        await ctx.send("Odświeżam baze danych postaci z lola")

    @command()
    async def tft(self, ctx, times: try_convert = 2):
        types = ['Infiltrator', 'Sorcerer', 'Blademaster', 'Brawler', 'Mystic', 'Protector', 'Sniper', 'Blaster',
                 'Demolitionist', 'Mana-Reaver', 'Vanguard', 'Dark Star', 'Mech Pilot', 'Cybernetic', 'Star Guardian',
                 'Chrono', 'Celestial', 'Space Pirate', 'Void', 'Rebel']
        random.shuffle(types)
        times = times if 0 < times < len(types) else 2
        msg = []
        for _ in range(times):
            msg.append(types.pop())
        await ctx.send(' i '.join(msg))


def setup(bot):
    bot.add_cog(LeagueOfLegends(bot))

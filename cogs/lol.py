from discord.ext import commands
from discord.ext.commands import command
import random
from cogs.webscraping import fetch_champions
from dbwrapper import query_insert
import typing


class LeagueOfLegends(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(aliases=('toplane',))
    async def top(self, ctx, times: typing.Optional[int] = 1):
        """Wylosuj sobie topa"""
        await fetch_champions(ctx, times, "top", 0xCC0000)

    @command(aliases=('jgl',))
    async def jungle(self, ctx, times: typing.Optional[int] = 1):
        """Wylosuj sobie jungle"""
        await fetch_champions(ctx, times, "jungle", 0x339933)

    @command(aliases=('middle', 'midlane'))
    async def mid(self, ctx, times: typing.Optional[int] = 1):
        """Wylosuj sobie mida"""
        await fetch_champions(ctx, times, "middle", 0xFFCC33)

    @command()
    async def adc(self, ctx, times: typing.Optional[int] = 1):
        """Wylosuj sobie adc"""
        await fetch_champions(ctx, times, "adc", 0x3399FF)

    @command(aliases=('support',))
    async def supp(self, ctx, times: typing.Optional[int] = 1):
        """Wylosuj sobie suppa"""
        await fetch_champions(ctx, times, "support", 0xFF99FF)

    @command()
    async def team(self, ctx, times: typing.Optional[int] = 1):
        """Wylosuj sobie cały team"""
        await fetch_champions(ctx, times, 'team', 0xA652BB)

    @command()
    async def resetdb(self, ctx):
        """Zaktualizuj bazę danych z champion.gg i lolwiki"""
        query_insert('DELETE FROM lolchamps')
        query_insert('DELETE FROM rules where type="lolchamps"')
        await ctx.send("Odświeżam baze danych postaci z lola")

    @command()
    async def tft(self, ctx, times: typing.Optional[int] = 2):
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

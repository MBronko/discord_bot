from discord.ext import commands
import random
from cogs.webscraping import fetch_champions
from manage_db import query_insert


class LeagueOfLegends(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=('toplane',))
    async def top(self, ctx, times=''):
        """Wylosuj sobie topa"""
        await fetch_champions(ctx, times, "top")

    @commands.command(aliases=('jgl',))
    async def jungle(self, ctx, times=''):
        """Wylosuj sobie jungle"""
        await fetch_champions(ctx, times, "jungle")

    @commands.command(aliases=('middle', 'midlane'))
    async def mid(self, ctx, times=''):
        """Wylosuj sobie mida"""
        await fetch_champions(ctx, times, "middle")

    @commands.command()
    async def adc(self, ctx, times=''):
        """Wylosuj sobie adc"""
        await fetch_champions(ctx, times, "adc")

    @commands.command(aliases=('support',))
    async def supp(self, ctx, times=''):
        """Wylosuj sobie suppa"""
        await fetch_champions(ctx, times, "support")

    @commands.command()
    async def team(self, ctx, times=''):
        """Wylosuj sobie cały team"""
        await fetch_champions(ctx, times)

    @commands.command()
    async def resetdb(self, ctx):
        """Zaktualizuj bazę danych z champion.gg i lolwiki"""
        query_insert('DELETE FROM lolchamps')
        query_insert('DELETE FROM rules where type="lolchamps"')
        await ctx.send("Odświeżam baze danych postaci z lola")

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
    bot.add_cog(LeagueOfLegends(bot))

from discord.ext import commands
from discord.ext.commands import command
from utils.LeagueWebScraping import display_champions, fetch_champions, fetch_data
from typing import Optional


class Leagueroll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(aliases=('toplane',))
    async def top(self, ctx, times: Optional[int] = 1):
        """Get random top champion"""
        await display_champions(ctx, times, "top", 0xCC0000)

    @command(aliases=('jgl',))
    async def jungle(self, ctx, times: Optional[int] = 1):
        """Get random jungle champion"""
        await display_champions(ctx, times, "jungle", 0x339933)

    @command(aliases=('middle', 'midlane'))
    async def mid(self, ctx, times: Optional[int] = 1):
        """Get random middle champion"""
        await display_champions(ctx, times, "mid", 0xFFCC33)

    @command()
    async def adc(self, ctx, times: Optional[int] = 1):
        """Get random adc champion"""
        await display_champions(ctx, times, "adc", 0x3399FF)

    @command(aliases=('supp',))
    async def support(self, ctx, times: Optional[int] = 1):
        """Get random support champion"""
        await display_champions(ctx, times, "support", 0xFF99FF)

    @command()
    async def team(self, ctx, times: Optional[int] = 1):
        """Get random champion for each role"""
        await display_champions(ctx, times, 'team', 0xA652BB)

    @command()
    async def refresh(self, ctx):
        """Refresh champion database"""
        fetch_urls = [data[0] for data in fetch_data]
        msg = 'Champions database was refreshed\nUsed sites:\n<{}>'.format('>\n<'.join(fetch_urls))
        if await fetch_champions(ctx):
            await ctx.send(msg)


def setup(bot):
    bot.add_cog(Leagueroll(bot))

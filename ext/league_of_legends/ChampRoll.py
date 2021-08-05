from discord.ext.commands import command, Cog, Context
from leaguetools.ChampRollTools import display_champions, fetch_champions, fetch_data
from typing import Optional


class ChampRoll(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(aliases=('toplane',))
    async def top(self, ctx: Context, times: Optional[int] = 1):
        """Get random top champion"""
        await display_champions(ctx, times, 'TOP', 0xCC0000)

    @command(aliases=('jgl',))
    async def jungle(self, ctx: Context, times: Optional[int] = 1):
        """Get random jungle champion"""
        await display_champions(ctx, times, 'JUNGLE', 0x339933)

    @command(aliases=('middle', 'midlane'))
    async def mid(self, ctx: Context, times: Optional[int] = 1):
        """Get random middle champion"""
        await display_champions(ctx, times, 'MIDDLE', 0xFFCC33)

    @command()
    async def adc(self, ctx: Context, times: Optional[int] = 1):
        """Get random adc champion"""
        await display_champions(ctx, times, 'BOTTOM', 0x3399FF)

    @command(aliases=('supp',))
    async def support(self, ctx: Context, times: Optional[int] = 1):
        """Get random support champion"""
        await display_champions(ctx, times, 'UTILITY', 0xFF99FF)

    @command()
    async def team(self, ctx: Context, times: Optional[int] = 1):
        """Get random champion for each role"""
        await display_champions(ctx, times, 'TEAM', 0xA652BB)

    @command()
    async def refresh(self, ctx: Context):
        """Refresh champion database"""
        fetch_urls = [data[0] for data in fetch_data]
        msg = 'Champions database was refreshed\nUsed sites:\n<{}>'.format('>\n<'.join(fetch_urls))
        if await fetch_champions(ctx):
            await ctx.send(msg)


def setup(bot):
    bot.add_cog(ChampRoll(bot))

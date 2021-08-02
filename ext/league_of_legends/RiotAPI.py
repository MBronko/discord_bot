from discord.ext.commands import command, Cog
from discord.ext.commands.context import Context
from leaguetools.RiotAPI.tasks import summoner_level, get_summoner


class RiotAPI(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def level(self, ctx: Context, *name: str):
        name = ''.join(name)
        if name:
            summoner = await get_summoner(name)
            if summoner:
                return await ctx.send(f'{summoner.name} has {summoner.level}lv.')

        await ctx.send('Summoner not found')


def setup(bot):
    bot.add_cog(RiotAPI(bot))

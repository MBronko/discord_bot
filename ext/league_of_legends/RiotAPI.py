from discord.ext.commands import command, Cog
from discord.ext.commands.context import Context

from utils.Common import GREEN_TICK, RED_X
from leaguetools.RiotAPI.tasks import get_summoner, get_champion, get_meraki_champion
from pyot.models import lol
from pyot.core.exceptions import NotFound


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

    @command()
    async def chest(self, ctx: Context, name: str = '', *champ_name: str):
        summoner = await get_summoner(name)

        if not summoner:
            return await ctx.send('Summoner not found')

        champ = await get_champion(champ_name)

        if not champ:
            return await ctx.send('Champion not found')

        champ_mastery = None

        try:
            champ_mastery = await lol.ChampionMastery(summoner_id=summoner.id, champion_id=champ.id).get()
        except NotFound:
            pass

        if champ_mastery and champ_mastery.chest_granted:
            inner_msg = f'unavailable {RED_X}'
        else:
            inner_msg = f'available {GREEN_TICK}'

        await ctx.send(f'Chest for {summoner.name} on {champ.name} is {inner_msg}')


def setup(bot):
    bot.add_cog(RiotAPI(bot))

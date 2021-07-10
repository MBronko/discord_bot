from discord.ext import commands
from discord.ext.commands import command
import typing


class Messages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(aliases=('delete', 'usun', 'fetusdeletus', 'del', 'purge', 'clear'))
    @commands.has_permissions(manage_messages=True)
    async def dele(self, ctx, times: typing.Optional[int] = 1):
        """Usuń ileś tam wiadomości"""
        max_limit = 50
        # TODO dele settings
        limit = times + 2 if times <= max_limit else max_limit
        await ctx.send("bedzie usuwanko")
        await ctx.channel.purge(limit=limit)


def setup(bot):
    bot.add_cog(Messages(bot))

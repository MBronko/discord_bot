from discord.ext import commands
from discord.ext.commands import command
from typing import Optional


class Messages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(aliases=('dele', 'del', 'purge'))
    @commands.has_permissions(manage_messages=True)
    async def delete(self, ctx, times: Optional[int] = 1):
        """Remove a number of messages"""
        print(times)
        max_limit = 50
        # TODO dele settings
        limit = times + 2 if times <= max_limit else max_limit
        await ctx.send("Removing messages")
        await ctx.channel.purge(limit=limit)


def setup(bot):
    bot.add_cog(Messages(bot))

from discord.ext import commands
from discord.ext.commands import command
import random


class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def choose(self, ctx, *choices: str):
        """Choose one random thing"""
        if choices:
            await ctx.send(random.choice(choices))

    @command()
    async def rng(self, ctx, min_val=0, max_val=10):
        try:
            min_val = int(min_val)
        except ValueError:
            min_val = 0
        try:
            max_val = int(max_val)
        except ValueError:
            max_val = 10
        await ctx.send(random.randint(min_val, max_val))

    @command()
    async def coinflip(self, ctx):
        await ctx.send(random.choice(['heads', 'tails']))


def setup(bot):
    bot.add_cog(Random(bot))

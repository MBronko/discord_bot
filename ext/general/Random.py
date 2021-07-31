from discord.ext.commands import command, Cog, Context
import random


class Random(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def choose(self, ctx: Context, *choices: str):
        """Choose one random thing from list"""
        if choices:
            await ctx.send(random.choice(choices))

    @command(aliases=('subset',))
    async def sample(self, ctx: Context, *choices: str):
        """Get a random subset"""
        length = len(choices)
        if length == 0:
            return await ctx.send(f'{ctx.prefix}sample \'set of choices\' [size of subset]')
        if length == 1:
            return await ctx.send(choices[0])
        try:
            n = int(choices[-1])
            n = min(length - 1, n)
            n = max(n, 1)
            choices = choices[:-1]
        except ValueError:
            n = 1
        await ctx.send(' '.join(random.sample(choices, n)))

    @command()
    async def rng(self, ctx: Context, min_val=0, max_val=10):
        """Get a random number in bounds"""
        try:
            min_val = int(min_val)
        except ValueError:
            min_val = 0
        try:
            max_val = int(max_val)
        except ValueError:
            max_val = 10

        if min_val > max_val:
            min_val, max_val = max_val, min_val
        await ctx.send(str(random.randint(min_val, max_val)))

    @command()
    async def coinflip(self, ctx: Context):
        """Roll heads or tails"""
        await ctx.send(random.choice(['heads', 'tails']))


def setup(bot):
    bot.add_cog(Random(bot))

from discord.ext import commands
from discord.ext.commands import command
from discord import Embed


class todolist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def todo(self, ctx):
        print('todo')

    @todo.command()
    async def create(self, ctx):
        print('add')
        emb = Embed()
        emb.add_field(name='siema', value='elo')
        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(todolist(bot))

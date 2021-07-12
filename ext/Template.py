from discord.ext import commands
from discord.ext.commands import command


class Template(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def template(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Template(bot))

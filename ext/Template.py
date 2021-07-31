from discord.ext.commands import command, Cog
from discord.ext.commands.context import Context


class Template(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def template(self, ctx: Context):
        pass


def setup(bot):
    bot.add_cog(Template(bot))

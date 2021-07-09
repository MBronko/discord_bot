from discord.ext import commands
from discord.ext.commands import command, errors
from src.utils.tools import get_extensions
from src.utils.models import Session, Rules, Leaguechamps


class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def reload(self, ctx):
        to_reload = get_extensions()
        to_unload = [key for key in self.bot.extensions.keys() if key not in to_reload]
        for extension in to_unload:
            self.bot.unload_extension(extension)
        for extension in get_extensions():
            try:
                self.bot.reload_extension(extension)
            except errors.ExtensionNotLoaded:
                self.bot.load_extension(extension)

        print("Reloaded extensions")
        await ctx.send("Reloaded extensions")

    @command()
    async def clear(self, ctx):
        with Session() as session:
            session.query(Rules).delete()
            session.query(Leaguechamps).delete()
            session.commit()
        print("Cleared database")
        await ctx.send("Cleared database")


def setup(bot):
    bot.add_cog(Debug(bot))

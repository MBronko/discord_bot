from discord.ext import commands
from discord.ext.commands import command, errors
from utils.Tools import get_extensions
from utils.Models import Session, Base


class Debug(commands.Cog):
    """DEBUG"""

    def __init__(self, bot):
        self.bot = bot

    @command()
    @commands.is_owner()
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
    @commands.is_owner()
    async def cleardb(self, ctx):
        with Session() as session:
            for model in Base.registry.mappers:
                session.query(model.class_).delete()
            session.commit()

        print("Cleared database")
        await ctx.send("Cleared database")

    @command(aliases=('logout',))
    @commands.is_owner()
    async def stop(self, ctx):
        await ctx.send('Bye')
        await self.bot.close()


def setup(bot):
    bot.add_cog(Debug(bot))

from discord.ext import commands
from manage_db import *


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=('chpref', 'pref', 'prefix'))
    async def changepref(self, ctx, prefix):
        """Zmień se prefixa"""
        if ctx.guild is None:
            return
        if query_select('SELECT * FROM rules WHERE server = ? AND type="prefix"', (ctx.guild.id,)):
            query_insert('UPDATE rules SET info = ? WHERE server = ?', (prefix, ctx.guild.id))
        else:
            query_insert('INSERT INTO rules (server, type, info) values (?, "prefix", ?)', (ctx.guild.id, prefix))
        await ctx.send("Zmieniono prefix na `{}`".format(prefix if prefix != '' else ' '))


def setup(bot):
    bot.add_cog(Settings(bot))

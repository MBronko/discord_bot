from discord.ext import commands
from discord.ext.commands import command
from manage_db import query_select, query_insert


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(aliases=('chpref', 'pref', 'prefix'))
    @commands.guild_only()
    async def changepref(self, ctx, prefix):
        """Zmień se prefixa"""
        blacklist = [
            'jd'
        ]
        if ctx.guild is None:
            await ctx.send('Działa tylko na serwerach')
            return
        if prefix in blacklist:
            await ctx.send('Ten prefix jest na blackliście')
            return
        if len(prefix) > 5:
            await ctx.send('No chyba troche za długie xD')
            return
        if query_select('SELECT * FROM rules WHERE server = ? AND type="prefix"', (ctx.guild.id,)):
            query_insert('UPDATE rules SET info = ? WHERE server = ?', (prefix, ctx.guild.id))
        else:
            query_insert('INSERT INTO rules (server, type, info) values (?, "prefix", ?)', (ctx.guild.id, prefix))
        await ctx.send("Zmieniono prefix na `{}`".format(prefix if prefix != '' else ' '))


def setup(bot):
    bot.add_cog(Settings(bot))

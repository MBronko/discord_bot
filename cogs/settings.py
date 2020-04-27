from discord.ext import commands
from functions import get_prefix
from discord.ext.commands import command
from manage_db import query_select, query_insert
from discord import Embed


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.guild_only()
    async def settings(self, ctx):
        if not ctx.invoked_subcommand:
            prefix = get_prefix(self.bot, ctx)[-1]
            embed = Embed(description='Change bot settings here')
            embed.set_author(name='Mimi mentor settings', icon_url=self.bot.user.avatar_url)
            embed.add_field(name='Prefix', value='`' + prefix + 'settings prefix`')
            embed.add_field(name='empty', value='`' + prefix + 'settings empty`')
            embed.add_field(name='empty', value='`' + prefix + 'settings empty`')
            embed.add_field(name='empty', value='`' + prefix + 'settings empty`')
            embed.add_field(name='empty', value='`' + prefix + 'settings empty`')
            embed.add_field(name='empty', value='`' + prefix + 'settings empty`')
            await ctx.send(embed=embed)

    @settings.command(alias='pref')
    async def prefix(self, ctx, new_prefix=''):
        blacklist = [
            'jd'
        ]
        if new_prefix == '':
            query_insert('UPDATE rules SET info = ? WHERE server = ?', (new_prefix, ctx.guild.id))
            prefix = get_prefix(self.bot, ctx)[-1]
            embed = Embed(description='Change prefix to address bot commands')
            embed.set_author(name='Mimi mentor settings', icon_url=self.bot.user.avatar_url)
            embed.add_field(name='Actual prefix', value='`' + prefix + '`', inline=False)
            embed.add_field(name='Usage', value='`' + prefix + 'settings prefix [new prefix]`')
            await ctx.send(embed=embed)
        else:
            if new_prefix in blacklist:
                return await ctx.send('Ten prefix jest na blackliście')
            if len(new_prefix) > 3:
                return await ctx.send('No chyba troche za długie xD')
            if query_select('SELECT * FROM rules WHERE server = ? AND type="prefix"', (ctx.guild.id,)):
                query_insert('UPDATE rules SET info = ? WHERE server = ?', (new_prefix, ctx.guild.id))
            else:
                query_insert('INSERT INTO rules (server, type, info) values (?,"prefix",?)', (ctx.guild.id, new_prefix))
            await ctx.send("Zmieniono prefix na `{}`".format(new_prefix if new_prefix != '' else ' '))

    # @prefix.command()
    # async def add(self, ctx):
    #     embed = Embed()
    #     embed.add_field(name="test3", value="test3")
    #     await ctx.send(embed=embed)

    # @commands.command(aliases=('chpref', 'pref', 'prefix'))
    # async def changepref(self, ctx, prefix):
    #     """Zmień se prefixa"""


def setup(bot):
    bot.add_cog(Settings(bot))

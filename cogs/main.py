from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions
from manage_db import query_selectall
import discord
import random
import asyncio
from functions import tryconvert


class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command()
    # async def kick(self, ctx, member: discord.User):
    #     # if ctx.author.
    #     print(member.avatar_url)

    @commands.command(aliases=('logout',))
    async def stop(self, ctx):
        """Wyłącz bota xd"""
        await self.bot.logout()

    @commands.command(aliases=('delete', 'usun', 'fetusdeletus', 'del', 'purge', 'clear'))
    # @commands.has_permissions(manage_messages=True)
    async def dele(self, ctx, times: tryconvert = 0):
        """Usuń ileś tam wiadomości"""
        limit = times + 2 if times <= 50 else 50
        await ctx.send("bedzie usuwanko")
        await asyncio.sleep(.5)
        await ctx.channel.purge(limit=limit)

    # @dele.error
    # async def kick_error(self, ctx, error):
    #     raise
        # return
        # if isinstance(error, MissingPermissions):
        #     await ctx.send("Musisz mieć permisje do usuwania wiadomości")

    @commands.command()
    async def logs(self, ctx):
        for log in query_selectall('SELECT * FROM logs ORDER BY time ASC'):
            print(log)

    @commands.command()
    async def avatar(self, ctx, member: discord.User):
        """Ukradnij komuś avatarek"""
        await ctx.send(member.avatar_url)

    @commands.command(aliases=('siemano', 'hejka', 'czesc', 'witam'))
    async def eluwa(self, ctx):
        """Przywitaj się"""
        await ctx.send('no siemano')

    @commands.command(aliases=('test',))
    async def add(self, ctx, *numbers: tryconvert):
        """Dodej se ileś liczb."""
        await ctx.send(sum(numbers))

    @commands.command(aliases=('rng', 'RNG', 'wybierz', 'losulosu'))
    async def choose(self, ctx, *choices: str):
        """Wybierz za mnie :v oddziel możliwości spacją"""
        if choices:
            await ctx.send(random.choice(choices))

    @commands.command()
    # async def repeat(self, ctx, *, content, times: tryconvert):
    async def repeat(self, ctx, *, content):
        """Powtórz wiadomość pare razy"""
        print(content)
        # if times:
        #     print("{} powtarza {} - {} razy".format(ctx.author, content, times))
        #     for i in range(times if times <= 20 else 20):
        #         await ctx.send(content)
        #         await asyncio.sleep(1)


def setup(bot):
    bot.add_cog(Main(bot))

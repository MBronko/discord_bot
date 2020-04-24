from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions
import discord
import random
import asyncio


class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kick(self, ctx, member: discord.User):
        # if ctx.author.
        print(member.avatar_url)

    @commands.command()
    async def stop(self, ctx):
        """Wyłącz bota"""
        await self.bot.logout()

    @commands.command(aliases=('delete', 'usun', 'fetusdeletus', 'del', 'purge', 'clear'))
    @commands.has_permissions(manage_messages=True)
    async def dele(self, ctx, times):
        """Usuń ileś tam wiadomości"""
        # if ctx.author.
        try:
            limit = int(times) + 1 if int(times) <= 100 else 100
            await ctx.send("bedzie usuwanko", delete_after=1)
            await asyncio.sleep(2)
            await ctx.channel.purge(limit=limit)
        except ValueError:
            await ctx.send("liczbami upośledziu", delete_after=2)

    @dele.error
    async def kick_error(error, ctx):
        if isinstance(error, MissingPermissions):
            await ctx.send("Musisz mieć permisje do usuwania wiadomości")
            await asyncio.sleep(1)
            await ctx.channel.purge(limit=2)

    @commands.command()
    async def avatar(self, ctx, member: discord.User):
        """Ukradnij komuś avatarek"""
        await ctx.send(member.avatar_url)

    @commands.command(aliases=('siemano', 'hejka', 'czesc', 'witam'))
    async def eluwa(self, ctx):
        """Przywitaj się"""
        await ctx.send('no siemano')

    @commands.command()
    async def add(self, ctx, left: int, right: int):
        """Dodej se dwie liczby."""
        await ctx.send(left + right)

    @commands.command(aliases=('rng', 'RNG', 'wybierz', 'losulosu'))
    async def choose(self, ctx, *choices: str):
        """Wybierz za mnie :v oddziel możliwości spacją"""
        await ctx.send(random.choice(choices))

    @commands.command()
    async def repeat(self, ctx, content, times: int, ):
        """Powtórz wiadomość pare razy"""
        print("{} powtarza {} - {} razy".format(ctx.author, content, times))
        for i in range(times if times <= 20 else 20):
            await ctx.send(content)
            await asyncio.sleep(1)


def setup(bot):
    bot.add_cog(Main(bot))

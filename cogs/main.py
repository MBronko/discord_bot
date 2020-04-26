from discord.ext import commands
from discord.ext.commands import command
from manage_db import query_selectall
import discord
import random
import asyncio
from functions import try_convert


class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=""):
        if ctx.author.top_role > member.top_role:
            reason = '{}: {}'.format(ctx.author.display_name, reason)
            await ctx.guild.kick(member, reason=reason)
            await ctx.send(f"{member.display_name} został wyrzucony z serwera")
        else:
            await ctx.send("Osoba którą chcesz kicknąć ma za wysoką rangę")

    @command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=""):
        if ctx.author.top_role > member.top_role:
            reason = '{}: {}'.format(ctx.author.display_name, reason)
            await ctx.guild.ban(member, reason=reason, delete_message_days = 0)
            await ctx.send(f"{member.display_name} został zbanowany z serwera")
        else:
            await ctx.send("Osoba którą chcesz zbanować ma za wysoką rangę")

    @command(aliases=('logout',))
    async def stop(self, ctx):
        """Wyłącz bota xd"""
        await self.bot.logout()

    @command(aliases=('delete', 'usun', 'fetusdeletus', 'del', 'purge', 'clear'))
    @commands.has_permissions(manage_messages=True)
    async def dele(self, ctx, times: try_convert = 0):
        """Usuń ileś tam wiadomości"""
        limit = times + 2 if times <= 50 else 50
        await ctx.send("bedzie usuwanko")
        await asyncio.sleep(.5)
        await ctx.channel.purge(limit=limit)

    @command()
    async def logs(self, ctx):
        for log in query_selectall('SELECT * FROM logs ORDER BY time ASC'):
            print(log)

    @command()
    async def avatar(self, ctx, member: discord.User):
        """Ukradnij komuś avatarek"""
        await ctx.send(member.avatar_url)

    @command(aliases=('siemano', 'hejka', 'czesc', 'witam'))
    async def eluwa(self, ctx):
        """Przywitaj się"""
        await ctx.send('no siemano')

    @command()
    async def add(self, ctx, *numbers: try_convert):
        """Dodej se ileś liczb."""
        await ctx.send(sum(numbers))

    @command(aliases=('rng', 'RNG', 'wybierz', 'losulosu'))
    async def choose(self, ctx, *choices: str):
        """Wybierz za mnie :v oddziel możliwości spacją"""
        if choices:
            await ctx.send(random.choice(choices))

    @command()
    async def repeat(self, ctx, *content):
        """Powtórz wiadomość pare razy"""
        if content:
            content = list(content)
            if len(content) >= 2:
                try:
                    popped = int(content[-1])
                    times = popped if popped <= 20 else 20
                    content.pop()
                except ValueError:
                    times = 1
            else:
                times = 1
            print("{} powtarza {} - {} razy".format(ctx.author, "\"" + " ".join(content) + "\"", times))
            for i in range(times):
                await ctx.send(" ".join(content))
                await asyncio.sleep(1)


def setup(bot):
    bot.add_cog(Main(bot))

from discord.ext import commands
from discord.ext.commands import command
# import discord.Embed
from manage_db import query_selectall
import discord
import random
import asyncio
from time import strftime
import time
from functions import try_convert


class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def henlo(self, ctx, members: commands.Greedy[discord.Member]):
        await ctx.send("henlo "+" ".join(map(lambda x: x.mention, members)))

    @command()
    async def info(self, ctx, member: discord.Member):
        embed = discord.Embed(title="Info o gościu", colour=0x00ffff)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_author(name=member.display_name, icon_url=member.avatar_url)

        embed.add_field(name="Display Name", value=member.display_name, inline=True)
        embed.add_field(name="Discriminator", value=member.discriminator, inline=True)
        embed.add_field(name="Created At", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name="Joined At", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(name="Status", value=member.status, inline=False)
        embed.add_field(name="Roles", value=" ".join(list(map(lambda x: x.mention, member.roles))[:0:-1]), inline=False)
        embed.set_footer(text="Displayed time is in UTC")
        await ctx.send(embed=embed)

    @command()
    async def mock(self, ctx, *, msg):
        """tOtAlNiE nIe MaM pOjEcIa Co To RoBi"""
        mock = ''
        upper = False
        for letter in msg:
            if upper:
                mock += letter.upper()
            else:
                mock += letter.lower()
            if letter != " ":
                upper = not upper
        await ctx.message.delete()
        await ctx.send(mock)

    @command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, members: commands.Greedy[discord.Member], *, reason=""):
        for member in members:
            if ctx.author.top_role > member.top_role:
                reason = '{}: {}'.format(ctx.author.display_name, reason)
                await ctx.guild.kick(member, reason=reason)
                await ctx.send(f"{member.display_name} został wyrzucony z serwera")
            else:
                await ctx.send(f"Nie możesz kicknąć {member.display_name}, ponieważ ma za wysoką rangę")

    @command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, members: commands.Greedy[discord.Member], *, reason=""):
        for member in members:
            if ctx.author.top_role > member.top_role:
                reason = '{}: {}'.format(ctx.author.display_name, reason)
                await ctx.guild.ban(member, reason=reason, delete_message_days = 0)
                await ctx.send(f"{member.display_name} został zbanowany z serwera")
            else:
                await ctx.send(f"Nie możesz zbanować {member.display_name}, ponieważ ma za wysoką rangę")

    @command(aliases=('logout','kys'))
    async def stop(self, ctx):
        """Wyłącz bota xd"""
        if ctx.guild.owner == ctx.author:
            await ctx.send('No to ja spadam xD')
            await self.bot.logout()
        else:
            await ctx.send('No na pewno xD')

    @command()
    async def test(self, ctx):
        def check_func(message):
            return message.content == "przestan" and message.channel == ctx.channel
        while True:
            print("xd")
            try:
                await self.bot.wait_for('message', timeout=1, check=check_func)
            except asyncio.TimeoutError:
                continue
            else:
                break
        print('koniec')

    @command(aliases=('delete', 'usun', 'fetusdeletus', 'del', 'purge', 'clear'))
    @commands.has_permissions(manage_messages=True)
    async def dele(self, ctx, times=''):
        """Usuń ileś tam wiadomości"""
        times = try_convert(times, 1)
        limit = times + 2 if times <= 50 else 50
        await ctx.send("bedzie usuwanko")
        await asyncio.sleep(.5)
        await ctx.channel.purge(limit=limit)

    @command()
    async def logs(self, ctx):
        for log in query_selectall('SELECT * FROM logs ORDER BY time ASC'):
            print(log)

    @command()
    async def avatar(self, ctx, member: discord.Member):
        """Ukradnij komuś avatarek"""
        embed = discord.Embed()
        embed.set_author(name=member.display_name, url=member.avatar_url)
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)

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
                await asyncio.sleep(.5)


def setup(bot):
    bot.add_cog(Main(bot))

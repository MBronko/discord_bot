from discord.ext import commands
from discord.ext.commands import command
# import discord.Embed
import discord
import requests
from src.utils.convert import convert_default
from src.utils.tools import get_prefix


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def info(self, ctx, members: commands.Greedy[discord.Member], sink=None):
        """Show info about users"""
        if not members and sink is not None:
            await ctx.send('Cant find specified user')
        for member in members:
            info_types = [
                {'name': 'Display Name', 'value': member.display_name, 'inline': True},
                {'name': 'Discriminator', 'value': member.discriminator, 'inline': True},
                {'name': 'Created At', 'value': member.created_at.strftime("%Y-%m-%d %H:%M:%S"), 'inline': False},
                {'name': 'Joined At', 'value': member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), 'inline': False},
                {'name': 'ID', 'value': member.id, 'inline': False},
                {'name': 'Status', 'value': member.status, 'inline': False},
                {'name': 'Roles', 'value': " ".join([x.mention for x in member.roles][:0:-1]), 'inline': False}
            ]
            embed = discord.Embed(title="Info o gościu", colour=0x00ffff)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_author(name=member.display_name, icon_url=member.avatar_url)

            for types in info_types:
                embed.add_field(name=types['name'], value=types['value'], inline=types['inline'])
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
    async def avatar(self, ctx, member: discord.Member):
        """Ukradnij komuś avatarek"""
        embed = discord.Embed()
        embed.set_author(name=member.display_name, url=member.avatar_url)
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)

    @command(aliases=('siemano', 'eluwa'))
    async def hello(self, ctx):
        """Przywitaj się"""
        await ctx.send('henlo')

    @command()
    async def gitara(self, ctx):
        await ctx.send('siema')

    @command(aliases=('link',))
    async def shorten(self, ctx, link):
        r = requests.post("https://bronko.me", data={'shorten': link}).text.strip()
        msg = f"<{r}>" if r != "Segmentation fault" else "Invalid URL"
        await ctx.send(msg)

    @command()
    async def add(self, ctx, *numbers: convert_default()):
        """Add numbers"""
        await ctx.send(sum(numbers))

    @command()
    async def repeat(self, ctx, *content: str):
        """Powtórz wiadomość pare razy"""
        length = len(content)
        if length == 0:
            await ctx.send(f'{get_prefix(self.bot, ctx, with_mention=False)}repeat `message` [times]')
        elif length == 1:
            await ctx.send(content[0])
        else:
            try:
                times = int(content[-1])
                times = times if times < 10 else 10
                content_str = " ".join(content[:-1])
            except ValueError:
                times = 1
                content_str = " ".join(content)

            for i in range(times):
                await ctx.send(content_str)


def setup(bot):
    bot.add_cog(General(bot))

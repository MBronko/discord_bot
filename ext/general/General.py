from discord.ext import commands
from discord.ext.commands import command
from utils.Convert import convert_default
from utils.Common import MAX_REPEAT
from discord import Embed
import requests


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def info(self, ctx):
        """Show info about users"""
        for user in ctx.message.mentions:
            info_types = [
                ['Display Name', user.display_name, True],
                ['Discriminator', user.discriminator, True],
                ['Created At', user.created_at.strftime('%Y-%m-%d %H:%M:%S'), False],
                ['Joined At', user.joined_at.strftime('%Y-%m-%d %H:%M:%S'), False],
                ['ID', user.id, False],
                ['Status', user.status, False],
                ['Roles', ' '.join([x.mention for x in user.roles][1:]), False]
            ]
            embed = Embed(title="User info", color=0x00ffff)
            embed.set_thumbnail(url=user.avatar_url)
            embed.set_author(name=user.display_name, icon_url=user.avatar_url)

            for types in info_types:
                embed.add_field(name=types[0], value=types[1], inline=types[2])
            embed.set_footer(text="UTC time zone was used in timestamps")
            await ctx.send(embed=embed)

    @command()
    async def mock(self, ctx, *, msg):
        """Mock sentence lIkE tHiS"""
        await ctx.message.delete()
        # TODO Create spongebob meme
        await ctx.send(''.join([elem.upper() if idx % 2 else elem.lower() for idx, elem in enumerate(msg)]))

    @command()
    async def avatar(self, ctx):
        """Show avatar of specified user"""
        for user in ctx.message.mentions:
            embed = Embed()
            embed.set_author(name=user.display_name, url=user.avatar_url)
            embed.set_image(url=user.avatar_url)
            await ctx.send(embed=embed)

    @command(aliases=('siemano', 'eluwa'))
    async def hello(self, ctx):
        """Say henlo"""
        await ctx.send('henlo')

    @command()
    async def gitara(self, ctx):
        """Siema"""
        await ctx.send('siema')

    @command(aliases=('link',))
    async def shorten(self, ctx, link):
        """Shorten your link"""
        r = requests.post("https://bronko.me", data={'shorten': link}).text.strip()
        msg = f"<{r}>" if r != "Segmentation fault" else "Invalid URL"
        await ctx.send(msg)

    @command()
    async def add(self, ctx, *numbers: convert_default()):
        """Add numbers"""
        await ctx.send(sum(numbers))

    @command()
    async def repeat(self, ctx, *content: str):
        """Repeat message a number of times"""
        length = len(content)
        if length == 0:
            return await ctx.send(f'{ctx.prefix}repeat `message` [times]')
        if length == 1:
            return await ctx.send(content[0])

        try:
            times = int(content[-1])
            times = times if times < MAX_REPEAT else MAX_REPEAT
            content_str = " ".join(content[:-1])
        except ValueError:
            times = 1
            content_str = " ".join(content)

        for i in range(times):
            await ctx.send(content_str)


def setup(bot):
    bot.add_cog(General(bot))

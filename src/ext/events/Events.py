from discord.ext.commands import Cog
from datetime import datetime


class Events(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print('------\nLogged in as {}\n{}\n------'.format(self.bot.user.name, self.bot.user.id))

    @Cog.listener()
    async def on_command(self, ctx):
        try:
            guild_name = ctx.guild.name
            channel_name = ctx.channel.name
        except AttributeError:
            guild_name = ""
            channel_name = ""

        with open('../logs.txt', 'a') as file:
            file.write(f"{datetime.now()};{ctx.author.name}#{ctx.author.discriminator};{guild_name};{channel_name};{ctx.message.content}\n")


def setup(bot):
    bot.add_cog(Events(bot))

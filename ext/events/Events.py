from discord.ext.commands import Cog
from datetime import datetime


class Events(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print(f'------\nLogged in as {self.bot.user.name}\n{self.bot.user.id}\n------')

    @Cog.listener()
    async def on_command(self, ctx):
        with open('logs.txt', 'a') as file:
            to_log = [
                datetime.now(),
                ctx.author,
                ctx.guild,
                ctx.channel,
                ctx.message.content
            ]
            file.write(';'.join([str(x) for x in to_log]) + '\n')


def setup(bot):
    bot.add_cog(Events(bot))

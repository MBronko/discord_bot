from discord.ext.commands import Cog, Context
from discord import Message
from datetime import datetime


class Events(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print(f'------\nLogged in as {self.bot.user.name}\n{self.bot.user.id}\n------')

    @Cog.listener()
    async def on_command(self, ctx: Context):
        with open('logs.txt', 'a') as file:
            to_log = [
                datetime.now(),
                ctx.author,
                ctx.guild,
                ctx.channel,
                ctx.message.content
            ]
            file.write(';'.join([str(x) for x in to_log]) + '\n')

    @Cog.listener()
    async def on_message(self, msg: Message):
        nine_gag_prefix = 'https://img-9gag-fun.9cache.com/photo/'
        nine_gag_suffixes = ['av1.mp4']
        cont = msg.content
        if cont.startswith(nine_gag_prefix):
            for suffix in nine_gag_suffixes:
                if cont.endswith(suffix):
                    await msg.channel.send(cont[:-len(suffix)] + suffix[3:])


def setup(bot):
    bot.add_cog(Events(bot))

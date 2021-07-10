from discord.ext.commands import Cog
from discord.ext import commands
from src.utils.common import DEBUG
import traceback
import sys


class CommandErrorHandler(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        if DEBUG:
            print(f'Exception \'{error}\' in \'{ctx.command}\' command', file=sys.stderr)

        # if hasattr(ctx.command, 'on_error'):
        #     return

        # print(error, file=sys.stderr)
        ignored = (commands.CommandNotFound,)
        # error = getattr(error, 'original', error)
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            return await ctx.send(f'This command is disabled')

        if isinstance(error, commands.NoPrivateMessage):
            return await ctx.author.send('This command cannot be used in private message')

        # if isinstance(error, commands.BadArgument):
        #     get_member = [
        #         'avatar',
        #         'kick',
        #         'ban'
        #     ]
        #     if ctx.command.qualified_name in get_member:
        #         msg = 'Cant find specified user'
        #     else:
        #         msg = 'Error: BadArgument'
        #     return await ctx.send(msg)

        if isinstance(error, commands.MissingPermissions):
            return await ctx.send('You dont have permissions to use this command')

        # Print traceback for uncaught errors
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))

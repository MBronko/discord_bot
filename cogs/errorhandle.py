import traceback
import sys
from discord.ext import commands
import discord


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.CommandNotFound, commands.UserInputError)

        error = getattr(error, 'original', error)
        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except:
                pass

        # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
                return await ctx.send('I could not find that member. Please try again.')
        elif isinstance(error, commands.MissingPermissions):
            if ctx.command.qualified_name == 'dele':
                return await ctx.send("Musisz mieć permisje do usuwania wiadomości")

        # All other Errors not returned come here... And we can just print the default TraceBack.
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    # """Below is an example of a Local Error Handler for our command do_repeat"""
    #
    # @commands.command(name='repeat', aliases=['mimic', 'copy'])
    # async def do_repeat(self, ctx, *, inp: str):
    #     """A simple command which repeats your input!
    #     inp  : The input to be repeated"""
    #
    #     await ctx.send(inp)
    #
    # @do_repeat.error
    # async def do_repeat_handler(self, ctx, error):
    #     """A local Error Handler for our command do_repeat.
    #     This will only listen for errors in do_repeat.
    #     The global on_command_error will still be invoked after."""
    #
    #     # Check if our required argument inp is missing.
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         if error.param.name == 'inp':
    #             await ctx.send("You forgot to give me input to repeat!")
    #

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
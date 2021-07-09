import traceback
import sys
from discord.ext import commands
from discord.ext.commands import command
import discord


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        # ext.UserInputError
        ignored = (commands.CommandNotFound,)
        error = getattr(error, 'original', error)
        if isinstance(error, ignored):
            return

        # Disabled ext
        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f'Komenda {ctx.command} została wyłączona.')

        # No Private Message
        elif isinstance(error, commands.NoPrivateMessage):
            return await ctx.author.send('Ta komenda nie może być użyta w prywatnej wiadomości.')

        # Bad Argument
        elif isinstance(error, commands.BadArgument):
            # Specific answer to commmands
            get_member = [
                'avatar',
                'info',
                'kick',
                'ban'
            ]
            if ctx.command.qualified_name in get_member:
                msg = 'Nie mogę znaleźć podanej osoby'
            else:
                msg = 'Error: BadArgument'
            return await ctx.send(msg)
        # Missing Permission
        elif isinstance(error, commands.MissingPermissions):
            # Specific answer to commmands
            if ctx.command.qualified_name == 'dele':
                msg = "Musisz mieć permisje do usuwania wiadomości"
            elif ctx.command.qualified_name == 'kick':
                msg = "Musisz mieć permisje do kickowania innych"
            elif ctx.command.qualified_name == 'ban':
                msg = "Musisz mieć permisje do banowania innych"
            else:
                msg = "Nie masz permisji do tego"
            return await ctx.send(msg)

        # All other Errors not returned come here... And we can just print the default TraceBack.
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
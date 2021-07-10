from discord.ext import commands
from discord.ext.commands import command
import discord


class Users(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
                await ctx.guild.ban(member, reason=reason, delete_message_days=0)
                await ctx.send(f"{member.display_name} został zbanowany z serwera")
            else:
                await ctx.send(f"Nie możesz zbanować {member.display_name}, ponieważ ma za wysoką rangę")


def setup(bot):
    bot.add_cog(Users(bot))

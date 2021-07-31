from discord.ext import commands
from discord.ext.commands import command, Cog, Context
import discord


class Users(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: Context, members: commands.Greedy[discord.Member], *, reason=""):
        for member in members:
            if ctx.author.top_role > member.top_role:
                reason = '{}: {}'.format(ctx.author.display_name, reason)
                await ctx.guild.kick(member, reason=reason)
                await ctx.send(f"{member.display_name} został wyrzucony z serwera")
            else:
                await ctx.send(f'You cant kick {member.display_name}')

    @command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: Context, members: commands.Greedy[discord.Member], *, reason=""):
        for member in members:
            if ctx.author.top_role > member.top_role:
                reason = '{}: {}'.format(ctx.author.display_name, reason)
                await ctx.guild.ban(member, reason=reason, delete_message_days=0)
                await ctx.send(f'{member.display_name} was banned from the server')
            else:
                await ctx.send(f'You cant ban {member.display_name}')


def setup(bot):
    bot.add_cog(Users(bot))

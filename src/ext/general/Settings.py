from discord.ext import commands
from discord import Embed
from src.utils.tools import get_prefix
from src.utils.models import Session, Rules
from src.utils.common import PREFIX_BLACKLIST


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.guild_only()
    async def settings(self, ctx):
        """Change bot settings"""
        settings_list = [
            ('Prefix', 'prefix'),
            ('Info', 'info'),
            ('empty', 'empty'),
            ('empty', 'empty'),
            ('empty', 'empty'),
            ('empty', 'empty')
        ]
        if not ctx.invoked_subcommand:
            prefix = get_prefix(self.bot, ctx)[-1]
            embed = Embed(description='Change bot settings here')
            
            embed.set_author(name='Mimi mentor settings', icon_url=self.bot.user.avatar_url)
            for setting in settings_list:
                embed.add_field(name=setting[0], value=f"`{prefix}settings {setting[1]}`")
                
            await ctx.send(embed=embed)

    @settings.command(alias='pref')
    async def prefix(self, ctx, new_prefix=None):
        """Set prefix to address bot"""
        if new_prefix is None:
            prefix = get_prefix(self.bot, ctx, with_mention=False)
            embed = Embed(description='Set prefix to address bot')
            embed.set_author(name=f'{self.bot.user.name} settings', icon_url=self.bot.user.avatar_url)
            embed.add_field(name='Actual prefix', value=f'`{prefix}`', inline=False)
            embed.add_field(name='Usage', value=f'`{prefix}settings prefix [new prefix]`')
            return await ctx.send(embed=embed)
        else:
            if new_prefix in PREFIX_BLACKLIST:
                return await ctx.send('This prefix is blacklisted')
            if len(new_prefix) > 3:
                return await ctx.send('This prefix is too long')

            with Session() as session:
                actual_prefix = session.query(Rules).where(Rules.server == ctx.guild.id, Rules.type == 'prefix').first()

                if actual_prefix:
                    actual_prefix.value = new_prefix
                else:
                    new_rule = Rules()
                    new_rule.server = ctx.guild.id
                    new_rule.type = 'prefix'
                    new_rule.value = new_prefix
                    session.add(new_rule)
                session.commit()

            await ctx.send(f'Changed prefix to `{new_prefix}`')


def setup(bot):
    bot.add_cog(Settings(bot))

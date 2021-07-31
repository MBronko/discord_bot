from discord.ext import commands
from discord.ext.commands import Cog, Context
from discord import Embed
from utils.TodoListTools import generate_unique_id, create_todo_embed, parse_todo_args, update_list
from utils.Queries import get_todo_list, get_all_todo_lists, get_todo_sects
from utils.Models import Session, Todolist, TodoSect
from utils.Tools import fetch_message, random_color
from utils.Common import EMBED_EMPTY_VAL


class todolist(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.has_permissions(administrator=True)
    async def todo(self, ctx: Context):
        await ctx.message.delete()

    @todo.command()
    async def show(self, ctx: Context):
        with Session() as session:
            lists = get_all_todo_lists(session, ctx.guild.id)

        embed = Embed(color=random_color())

        if not lists:
            embed.add_field(name=EMBED_EMPTY_VAL, value='empty', inline=False)

        embed.set_author(name='Todo Lists')
        for item in lists:
            embed.add_field(name=item.title, value=item.todo_id, inline=False)

        await ctx.send(embed=embed)

    @todo.command()
    async def create(self, ctx: Context, *title: str):
        title = ' '.join(title)
        if title == '':
            title = 'Title'

        color = random_color()

        new_id = generate_unique_id(ctx.guild.id)

        with Session() as session:
            new_list = Todolist()
            new_list.todo_id = new_id
            new_list.server_id = ctx.guild.id
            new_list.title = title
            new_list.color = color

            session.add(new_list)
            session.commit()

        await ctx.invoke(self.recreate, new_id)

    @todo.command()
    async def recreate(self, ctx: Context, *args: str):
        todo_id, sink = await parse_todo_args(ctx, args)

        if not todo_id:
            return

        with Session() as session:
            res = get_todo_list(session, ctx.guild.id, todo_id)

            msg = await fetch_message(ctx, res.msg_id)
            if msg:
                await msg.delete()

            sections = get_todo_sects(session, ctx.guild.id, todo_id)

            embed = create_todo_embed(res, sections)
            new_msg = await ctx.send(embed=embed)

            res.msg_id = new_msg.id
            session.commit()

    @todo.command()
    async def delete(self, ctx: Context, *args: str):
        todo_id, sink = await parse_todo_args(ctx, args)

        if not todo_id:
            return

        with Session() as session:
            to_delete = get_todo_list(session, ctx.guild.id, todo_id)

            msg = await fetch_message(ctx, to_delete.msg_id)
            if msg:
                await msg.delete()

            session.query(TodoSect).where(TodoSect.server_id == ctx.guild.id, TodoSect.todo_id == todo_id).delete()
            session.delete(to_delete)

            session.commit()

    @todo.command()
    async def title(self, ctx: Context, *args: str):
        todo_id, args = await parse_todo_args(ctx, args)

        if not todo_id:
            return

        new_title = ' '.join(args)
        if new_title == '':
            new_title = 'Title'

        with Session() as session:
            todo_list = get_todo_list(session, ctx.guild.id, todo_id)

            todo_list.title = new_title
            session.commit()

        await update_list(ctx, todo_id)

    @todo.command()
    async def color(self, ctx: Context, *args: str):
        todo_id, args = await parse_todo_args(ctx, args)

        if not todo_id:
            return

        if not args:
            return await ctx.send('Please input color')

        try:
            color = int(args[0].strip('#'), 16)
        except ValueError:
            return await ctx.send('Please input valid hex color')

        color = max(0, min(color, 0xFFFFFF))

        with Session() as session:
            todo_list = get_todo_list(session, ctx.guild.id, todo_id)

            todo_list.color = color
            session.commit()

        await update_list(ctx, todo_id)


def setup(bot):
    bot.add_cog(todolist(bot))

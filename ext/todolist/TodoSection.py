from discord.ext.commands import Cog, Context
from discord.ext import commands
from utils.TodoListTools import parse_todo_args, parse_section_args, update_list
from utils.Queries import get_todo_list, get_todo_sects
from utils.Models import Session, TodoSect
from sqlalchemy import func


class todosection(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.has_permissions(administrator=True)
    async def section(self, ctx: Context):
        await ctx.message.delete()

    @section.command()
    async def add(self, ctx: Context, *args: str):
        todo_id, title = await parse_todo_args(ctx, args)
        if not todo_id:
            return

        title = ' '.join(title)
        if title == '':
            title = 'Section'

        with Session() as session:
            section = TodoSect()
            section.todo_id = todo_id
            section.server_id = ctx.guild.id
            section.title = title

            session.add(section)
            session.commit()

        await update_list(ctx, todo_id)

    @section.command()
    async def remove(self, ctx: Context, *args: str):
        todo_id, section_id, args = await parse_section_args(ctx, args)

        if not (todo_id and section_id):
            return

        with Session() as session:
            sections = get_todo_sects(session, ctx.guild.id, todo_id)
            section = sections[section_id - 1]

            session.delete(section)
            session.commit()

        await update_list(ctx, todo_id)

    @section.command()
    async def title(self, ctx: Context, *args: str):
        todo_id, section_id, args = await parse_section_args(ctx, args)

        if not (todo_id and section_id):
            return

        title = ' '.join(args)
        if title == '':
            title = 'Title'

        with Session() as session:
            sections = get_todo_sects(session, ctx.guild.id, todo_id)
            section = sections[section_id - 1]

            section.title = title

            session.commit()

        await update_list(ctx, todo_id)

    @section.command()
    async def content(self, ctx: Context, *args: str):
        todo_id, section_id, args = await parse_section_args(ctx, args)

        if not (todo_id and section_id):
            return

        value = ' '.join(args).replace('\\n', '\n')
        if value == '':
            value = 'Title'

        with Session() as session:
            sections = get_todo_sects(session, ctx.guild.id, todo_id)
            section = sections[section_id - 1]

            section.content = value
            session.commit()

        await update_list(ctx, todo_id)

    @section.command()
    async def done(self, ctx: Context, *args: str):
        todo_id, section_id, args = await parse_section_args(ctx, args)

        if not (todo_id and section_id):
            return

        with Session() as session:
            sections = get_todo_sects(session, ctx.guild.id, todo_id)
            section = sections[section_id - 1]

            section.done = not section.done
            session.commit()

        await update_list(ctx, todo_id)

    @section.command()
    async def move(self, ctx: Context, *args: str):
        todo_id, section_id, args = await parse_section_args(ctx, args)

        if not (todo_id and section_id):
            return

        if not args:
            return await ctx.send('Specify second list id')

        todo_id_2 = args[0]

        with Session() as session:
            todo_list_2 = get_todo_list(session, ctx.guild.id, todo_id_2)
            if not todo_list_2:
                return await ctx.send('Invalid second list id')

            sections = get_todo_sects(session, ctx.guild.id, todo_id)
            section = sections[section_id - 1]

            section.todo_id = todo_id_2
            section.timestamp = func.now()

            session.commit()

        await update_list(ctx, todo_id)
        await update_list(ctx, todo_id_2)

    @section.command()
    async def swap(self, ctx: Context, *args: str):
        todo_id, section_id, args = await parse_section_args(ctx, args)

        if not (todo_id and section_id):
            return

        if not args:
            return await ctx.send('Specify second section id')

        try:
            section_id_2 = int(args[0])

            with Session() as session:
                sections = get_todo_sects(session, ctx.guild.id, todo_id)
                if 1 <= section_id_2 <= len(sections):
                    section = sections[section_id - 1]
                    section_2 = sections[section_id_2 - 1]

                    section.timestamp, section_2.timestamp = section_2.timestamp, section.timestamp
                    session.commit()

                    return await update_list(ctx, todo_id)
        except ValueError:
            pass

        await ctx.send('Please input valid second section id')


def setup(bot):
    bot.add_cog(todosection(bot))

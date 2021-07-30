import string
import discord
from discord.ext import commands
from discord.ext.commands.context import Context
from utils.Models import Session, Todolist, TodoSect
from utils.Common import EMBED_EMPTY_VAL
from utils.Tools import random_color
from utils.Convert import convert_default
from utils.Queries import get_todo_list, get_all_todo_lists, get_todo_sects, get_todo_list_by_msg
from discord import Embed, NotFound
from typing import Optional
import random


def parse_id(list_id: str) -> str:
    return list_id.strip('#').upper()


def generate_unique_id(server_id: int) -> str:
    allowed_chars = list(string.ascii_uppercase) + list(range(10))
    length = 7

    new_id = ''
    check_if_exists = True
    while check_if_exists:
        new_id = ''.join([str(random.choice(allowed_chars)) for _ in range(length)])

        with Session() as session:
            check_if_exists = get_todo_list(session, server_id, new_id)
    return new_id


def create_todo_embed(todo_list: Todolist, sections: list[TodoSect] = None) -> Embed:
    embed = Embed(color=todo_list.color)
    embed.set_author(name=todo_list.title)
    if not sections:
        embed.add_field(name=EMBED_EMPTY_VAL, value='Empty')
    else:
        for idx, section in enumerate(sections, 1):
            done = '~~' if section.done else ''
            content = EMBED_EMPTY_VAL if section.content == '' else section.content

            def mark(val: str) -> str:
                return f'{done}{val}{done}'

            embed.add_field(name=f'{idx}) {mark(section.title)}', value=mark(content), inline=False)
    return embed


async def fetch_message(ctx: Context, msg_id: int) -> Optional[discord.Message]:
    try:
        return await ctx.fetch_message(msg_id)
    except NotFound:
        return None


async def update_list(ctx: Context, todo_id: str) -> None:
    with Session() as session:
        todo_list = get_todo_list(session, ctx.guild.id, todo_id)
        sections = get_todo_sects(session, ctx.guild.id, todo_id)
        for section in sections:
            print(section.title, section.timestamp)

    if not todo_list:
        return

    msg = await fetch_message(ctx, todo_list.msg_id)

    if not msg:
        return

    embed = create_todo_embed(todo_list, sections)
    await msg.edit(embed=embed)


async def todo_list_not_found(ctx: Context, todo_id: str) -> None:
    await ctx.send(f'list with id #{todo_id} doesnt exist')


def parse_todo_args(ctx: Context, args: tuple[str]) -> tuple[Optional[str], tuple[str]]:
    """Gets command context and arguments then returns todo_id and rest of args"""
    with Session() as session:
        # check if valid todo_list was referenced
        if ctx.message.reference:
            todo_list = get_todo_list_by_msg(session, ctx.guild.id, ctx.message.reference.message_id)
            if todo_list:
                return todo_list.todo_id, args

        # else check if first argument was walid todo_id
        if len(args) > 0:
            todo_list = get_todo_list(session, ctx.guild.id, args[0])

            if todo_list:
                return args[0], args[1:]

        return None, args


def parse_section_args(ctx: Context, args: tuple[str]) -> tuple[Optional[str], Optional[int], tuple[str]]:
    todo_id, args = parse_todo_args(ctx, args)

    if todo_id and len(args) > 0:
        try:
            section = int(args[0])
            with Session() as session:
                num = session.query(TodoSect).where(TodoSect.server_id == ctx.guild.id, TodoSect.todo_id == todo_id).count()

            if num > 0:
                section = max(1, min(section, num))
                section -= 1
                args = args[1:]
            else:
                section = None
        except ValueError:
            section = 0

        return todo_id, section, args
    return todo_id, None, args


class todolist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def todo(self, ctx: Context):
        with Session() as session:
            lists = session.query(Todolist).all()
            for lis in lists:
                print(f'{lis.id}, {lis.msg_id}, {lis.title}')

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
        if not title:
            title = 'Title'

        color = random_color()

        # embed = create_todo_embed(title, color)
        # msg = await ctx.send(embed=embed)

        new_id = generate_unique_id(ctx.guild.id)

        with Session() as session:
            new_list = Todolist()
            # new_list.msg_id = msg.id
            new_list.todo_id = new_id
            new_list.server_id = ctx.guild.id
            new_list.title = title
            new_list.color = color

            session.add(new_list)
            session.commit()

        await ctx.invoke(self.recreate, new_id)

    @todo.command()
    async def recreate(self, ctx: Context, todo_id: parse_id = ''):
        with Session() as session:
            res = get_todo_list(session, ctx.guild.id, todo_id)

            if not res:
                return await todo_list_not_found(ctx, todo_id)

            msg = await fetch_message(ctx, res.msg_id)
            if msg:
                await msg.delete()

            sections = get_todo_sects(session, ctx.guild.id, todo_id)

            embed = create_todo_embed(res, sections)
            new_msg = await ctx.send(embed=embed)

            res.msg_id = new_msg.id
            session.commit()

    @todo.command()
    async def delete(self, ctx: Context, todo_id: parse_id = ''):
        with Session() as session:
            to_delete = get_todo_list(session, ctx.guild.id, todo_id)

            if not to_delete:
                return await todo_list_not_found(ctx, todo_id)

            msg = await fetch_message(ctx, to_delete.msg_id)
            if msg:
                await msg.delete()

            session.query(TodoSect).where(TodoSect.server_id == ctx.guild.id, TodoSect.todo_id == todo_id).delete()
            session.delete(to_delete)

            session.commit()

    @todo.command()
    async def title(self, ctx):
        print(self, type(self))
        # values = ' '.join(value)

        # values = values.replace('\\n', '\n')

        # print(values)
        values = 'aewf'

        ipsum = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
        check = '✅'
        embed = Embed(color=random_color())
        embed.set_author(name='todo title')
        # embed.add_field(name='title', value=f'{check}{(EMBED_EMPTY_VAL + " ")*3}{ipsum}\n\n{check}{ipsum}', inline=False)
        # embed.add_field(name='1) title', value=ipsum, inline=False)
        # embed.add_field(name='2) ~~title~~', value=f'~~{ipsum}~~', inline=False)
        embed.add_field(name='3) title', value=values, inline=False)
        # embed.add_field(name='jd', value=value, inline=False)

        await ctx.send(embed=embed)


class todosection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def section(self, ctx: Context):
        # print(parse_section_args(ctx, args))
        print('section')

    @section.command()
    async def add(self, ctx: Context, *args: str):
        todo_id, title = parse_todo_args(ctx, args)
        if not todo_id:
            return await ctx.send('Cant find specified todo list')

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
    async def edit(self, ctx: Context, *args: str):
        todo_id, section, content = parse_section_args(ctx, args)

        if not todo_id:
            return await ctx.send('Cant find specified todo list')

        content = ' '.join(content)

        print(todo_id, section, content)


def setup(bot):
    bot.add_cog(todolist(bot))
    bot.add_cog(todosection(bot))

from discord.ext.commands.context import Context
from discord import Embed
from utils.Queries import get_todo_list, get_todo_sects, get_todo_list_by_msg
from utils.Models import Session, Todolist, TodoSect
from utils.Common import EMBED_EMPTY_VAL
from utils.Tools import fetch_message
from typing import Optional
import string
import random


def parse_id(list_id: str) -> str:
    return list_id.strip('#').upper()


def generate_unique_id(server_id: int, length: int = 7) -> str:
    allowed_chars = list(string.ascii_uppercase) + list(range(10))

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


async def update_list(ctx: Context, todo_id: str) -> None:
    with Session() as session:
        todo_list = get_todo_list(session, ctx.guild.id, todo_id)
        sections = get_todo_sects(session, ctx.guild.id, todo_id)

    if not todo_list:
        return

    msg = await fetch_message(ctx, todo_list.msg_id)

    if not msg:
        return

    embed = create_todo_embed(todo_list, sections)
    await msg.edit(embed=embed)


async def parse_todo_args(ctx: Context, args: tuple[str]) -> tuple[Optional[str], tuple[str]]:
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

        await ctx.send('Cant find specified list')
        return None, args


async def parse_section_args(ctx: Context, args: tuple[str]) -> tuple[Optional[str], Optional[int], tuple[str]]:
    todo_id, args = await parse_todo_args(ctx, args)

    if todo_id:
        if args:
            try:
                section = int(args[0])

                with Session() as session:
                    num_of_sections = session.query(TodoSect).where(TodoSect.server_id == ctx.guild.id,
                                                                    TodoSect.todo_id == todo_id).count()
                if num_of_sections > 0:
                    if 1 <= section <= num_of_sections:
                        return todo_id, section, args[1:]
                else:
                    await ctx.send('Specified list doesnt have any sections')
            except ValueError:
                pass

        await ctx.send('Please input valid section id')

    return todo_id, None, args

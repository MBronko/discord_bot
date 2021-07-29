import string

from discord.ext import commands
from discord.ext.commands import command
from discord.ext.commands.errors import CommandInvokeError
from utils.Models import Session, Todolist, TodoSect
from utils.Common import EMBED_EMPTY_VAL
from utils.Tools import random_color
from discord import Embed
import random


def parse_id(list_id: str) -> str:
    return list_id.strip('#').upper()


def generate_unique_id(server_id: int) -> str:
    id_len = 7
    allowed_chars = list(string.ascii_uppercase) + list(range(10))

    new_id = ''
    check_if_exists = True
    while check_if_exists:
        new_id = ''.join([str(random.choice(allowed_chars)) for _ in range(id_len)])

        with Session() as session:
            check_if_exists = session.query(Todolist).where(Todolist.server_id == server_id,
                                                            Todolist.todo_id == new_id).first()
    return new_id


def create_todo_embed(title: str, color: int, sections: list[TodoSect] = False) -> Embed:
    embed = Embed(color=color)
    embed.set_author(name=title)
    if not sections:
        embed.add_field(name=EMBED_EMPTY_VAL, value='Empty')
    else:
        for idx, section in enumerate(sections, 1):
            done = '~~' if section.done else ''

            def mark(val: str) -> str:
                return f'{done}{val}{done}'

            embed.add_field(name=f'{idx}) {mark(section.title)}', value=mark(section.content), inline=False)
    return embed


async def todo_list_not_found(ctx, todo_id):
    await ctx.send(f'list with id #{todo_id} doesnt exist')


class todolist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def todo(self, ctx):
        with Session() as session:
            lists = session.query(Todolist).all()
            for lis in lists:
                print(f'{lis.id}, {lis.msg_id}, {lis.title}')

    @todo.command()
    async def create(self, ctx, *title):
        title = ' '.join(title)
        if not title:
            title = 'Title'

        color = random_color()

        embed = create_todo_embed(title, color)
        msg = await ctx.send(embed=embed)

        new_id = generate_unique_id(ctx.guild.id)

        with Session() as session:
            new_list = Todolist()
            new_list.msg_id = msg.id
            new_list.todo_id = new_id
            new_list.server_id = ctx.guild.id
            new_list.title = title
            new_list.color = color

            session.add(new_list)
            session.commit()

    @todo.command()
    async def show(self, ctx):
        with Session() as session:
            lists = session.query(Todolist).where(Todolist.server_id == ctx.guild.id).all()

        embed = Embed(color=random_color())

        if not lists:
            embed.add_field(name='\u200b', value='empty', inline=False)

        embed.set_author(name='Todo Lists')
        for item in lists:
            embed.add_field(name=item.title, value=item.todo_id, inline=False)

        await ctx.send(embed=embed)


    @todo.command()
    async def recreate(self, ctx, todo_id: parse_id = ''):
        with Session() as session:
            res = session.query(Todolist).where(Todolist.server_id == ctx.guild.id, Todolist.todo_id == todo_id).first()

            if not res:
                return await todo_list_not_found(ctx, todo_id)

            try:
                msg = await ctx.fetch_message(res.msg_id)
                await msg.delete()
            except CommandInvokeError:
                print('asd')

            sects = session.query(TodoSect).where(TodoSect.server_id == ctx.guild.id, TodoSect.todo_id == todo_id).all()

            embed = create_todo_embed(res.title, res.color, sects)
            new_msg = await ctx.send(embed=embed)

            res.msg_id = new_msg.id
            session.commit()

        print(todo_id)

        # todo_id: str = ''):
        # todo_id = parse_id(todo_id)


    @todo.command()
    async def delete(self, ctx, todo_id: str = ''):
        todo_id = parse_id(todo_id)
        with Session() as session:
            to_delete = session.query(Todolist).where(Todolist.server_id == ctx.guild.id,
                                                      Todolist.todo_id == todo_id).first()

            if not to_delete:
                return await todo_list_not_found(ctx, todo_id)

            msg = await ctx.fetch_message(to_delete.msg_id)
            await msg.delete()
            session.query(TodoSect).where(TodoSect.server_id == ctx.guild.id, TodoSect.todo_id == todo_id).delete()
            session.delete(to_delete)

            session.commit()

    @todo.command()
    async def edit(self, ctx, title='', *value):
        values = ' '.join(value)

        values = values.replace('\\n', '\n')

        print(values)
        # print(ctx.message.reference.message_id)
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


def setup(bot):
    bot.add_cog(todolist(bot))

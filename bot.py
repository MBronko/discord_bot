import discord
from discord.ext import commands
import random
import asyncio
from create_db import create_db
import sqlite3

db_name = 'botdb.db'
create_db(db_name)
conn = sqlite3.connect(db_name)
cur = conn.cursor()
token = open('token.txt').readline().strip('\n')
default_prefix = ''
initial_extensions = [
    'cogs.lol',
]


def getprefix(bott, message):
    if message.guild is None:
        prefix = default_prefix
    else:
        server_id = message.guild.id
        cur.execute("SELECT info FROM rules WHERE server = ? AND type = 'prefix'", (server_id,))
        try:
            prefix = cur.fetchone()[0]
        except TypeError:
            prefix = default_prefix
    return commands.when_mentioned_or(prefix)(bott, message)


description = 'No siemano tutej so komendy do bota i w ogóle, jeżeli zapomnisz prefixu to możesz też wywołać ' \
              'komende pingując bota'
bot = commands.Bot(command_prefix=getprefix, description=description)

# 328935623144636426 mlp id
if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    game = discord.Game("gituuwa elo", type=1, url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    await bot.change_presence(activity=game)
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound) or isinstance(error, commands.errors.BadArgument):
        return
    raise error


@bot.command()
async def kick(ctx, member: discord.User):
    print(member.avatar_url)


@bot.command()
async def avatar(ctx, member: discord.User):
    """Ukradnij komuś avatarek"""
    await ctx.send(member.avatar_url)


@bot.command()
async def eluwa(ctx):
    """Przywitaj się"""
    await ctx.send('no siemano')


@bot.command()
async def add(ctx, left: int, right: int):
    """Dodej se dwie liczby."""
    await ctx.send(left + right)


@bot.command()
async def choose(ctx, *choices: str):
    """Wybierz za mnie :v oddziel możliwości spacją"""
    await ctx.send(random.choice(choices))


@bot.command()
async def repeat(ctx, content, times: int, ):
    """Powtórz wiadomość pare razy"""
    print("{} powtarza {} - {} razy".format(ctx.author, content, times))
    for i in range(times):
        await ctx.send(content)


@bot.command()
async def changepref(ctx, prefix):
    """Zmień se prefixa"""
    if ctx.guild is None:
        return
    cur.execute('SELECT * FROM rules WHERE server = ? AND type="prefix"', (ctx.guild.id,))
    if cur.fetchone():
        cur.execute('UPDATE rules SET info = ? WHERE server = ?', (prefix, ctx.guild.id))
    else:
        cur.execute('INSERT INTO rules (server, type, info) values (?, "prefix", ?)', (ctx.guild.id, prefix))
    conn.commit()
    await ctx.send("Zmieniono prefix na `{}`".format(prefix if prefix != '' else ' '))


@bot.command()
async def dele(ctx, times):
    """Usuń ileś tam wiadomości"""
    try:
        limit = int(times)+1 if int(times) <= 100 else 100
        await ctx.send("bedzie usuwanko", delete_after=1)
        await asyncio.sleep(2)
        await ctx.channel.purge(limit=limit)
    except ValueError:
        await ctx.send("liczbami upośledziu", delete_after=2)

bot.run(token)

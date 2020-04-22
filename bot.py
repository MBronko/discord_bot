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


def getprefix(bot, message):
    server_id = message.guild.id
    cur.execute("SELECT info FROM rules WHERE server = ? AND type = 'prefix'", (server_id,))
    try:
        prefix = cur.fetchone()[0]
    except TypeError:
        prefix = ''
    return prefix


description = 'No siemano tutej so komendy do bota i w ogóle'
bot = commands.Bot(command_prefix=getprefix, description=description)

# 328935623144636426 mlp id
@bot.event
async def on_ready():
    game = discord.Game("gituwa elo")
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
async def tft(ctx, times=''):
    try:
        times = int(times) if 20 >= int(times) > 0 and times != '' else 2
    except Exception:
        times = 2
    types = ['Infiltrator', 'Sorcerer', 'Blademaster', 'Brawler', 'Mystic', 'Protector', 'Sniper', 'Blaster',
             'Demolitionist', 'Mana-Reaver', 'Vanguard', 'Dark Star', 'Mech Pilot', 'Cybernetic', 'Star Guardian',
             'Chrono', 'Celestial', 'Space Pirate', 'Void', 'Rebel']
    random.shuffle(types)
    msg = ''
    for _ in range(times):
        msg += 'i ' + types.pop() + ' '
    await ctx.send(msg[2:])


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
        await asyncio.sleep(1)
        await ctx.channel.purge(limit=limit)
    except ValueError:
        await ctx.send("liczbami upośledziu", delete_after=2)

bot.run(token)

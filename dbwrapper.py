import sqlite3
import os

db_name = 'dcbot.db'


def create_db():
    if not os.path.isfile(db_name):
        f = open(db_name, 'w')
        f.close()

        conn = sqlite3.connect(db_name)
        c = conn.cursor()

        c.execute('''CREATE TABLE rules
                     (server TEXT, channel TEXT, user TEXT, type TEXT, value TEXT)''')

        c.execute('''CREATE TABLE logs
                     (user TEXT, server TEXT, channel TEXT, command TEXT, time TEXT)''')

        c.execute('''CREATE TABLE lolchamps
                     (champ TEXT, top TEXT, jungle TEXT, middle TEXT, adc TEXT, support TEXT)''')

        c.execute('''CREATE TABLE cahgame
                     (server TEXT, channel TEXT, user TEXT, game_id TEXT, round_id TEXT, type TEXT, flag TEXT, 
                     value TEXT, time TEXT)''')

        conn.commit()
        conn.close()


def query_select(sql, args=''):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute(sql, args)
    result = cur.fetchone()
    conn.close()
    return result


def query_selectall(sql, args='', focus_on_row=False):
    conn = sqlite3.connect(db_name)
    if focus_on_row:
        conn.row_factory = lambda cursor, row: row[0]
    cur = conn.cursor()
    cur.execute(sql, args)
    result = cur.fetchall()
    conn.close()
    return result


def query_insert(sql, args=''):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute(sql, args)
    conn.commit()
    conn.close()


def query_insertmany(sql, args=''):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.executemany(sql, args)
    conn.commit()
    conn.close()
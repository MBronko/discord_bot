import sqlite3
import os

db_name = 'botdb.db'


def create_db():
    if not os.path.isfile(db_name):
        f = open(db_name, 'w')
        f.close()

        conn = sqlite3.connect(db_name)
        c = conn.cursor()

        c.execute('''CREATE TABLE rules
                     (server TEXT, channel TEXT, user TEXT, type TEXT, info TEXT)''')

        c.execute('''CREATE TABLE logs
                     (user TEXT, server TEXT, channel TEXT, command TEXT, time TEXT)''')

        c.execute('''CREATE TABLE lolchamps
                     (champ TEXT, top TEXT, jungle TEXT, middle TEXT, adc TEXT, support TEXT)''')

        conn.commit()
        conn.close()


def query_select(sql, args=''):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute(sql, args)
    result = cur.fetchone()
    conn.close()
    return result


def query_selectall(sql, args=''):
    conn = sqlite3.connect(db_name)
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
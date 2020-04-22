import sqlite3
import os


def create_db(db_name):
    if not os.path.isfile(db_name):
        f = open(db_name, 'w')
        f.close()

        conn = sqlite3.connect(db_name)
        c = conn.cursor()

        c.execute('''CREATE TABLE rules
                     (server TEXT, channel TEXT, user TEXT, type TEXT, info TEXT)''')

        c.execute('''CREATE TABLE logs
                     (user TEXT, server TEXT, channel TEXT, command TEXT, time TEXT)''')

        conn.commit()
        conn.close()

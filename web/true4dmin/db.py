import sqlite3

conn = sqlite3.connect('./db/users.db')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, admin INTEGER)')

conn.commit()
conn.close()

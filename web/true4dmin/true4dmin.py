#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

FLAG = 'ETSIIT_CTF{Y0U_B3C4M3_4N_4DM1N}'

app = Flask(__name__)

# Flask-Session config
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'sup3rs3cr3tk3y!'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = request.form['admin']
        
        conn = sqlite3.connect('db/users.db')
        c = conn.cursor()

        # Check if user exists
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        result = c.fetchone()
        if result:
            return "El usuario ya existe", 409

        c.execute('INSERT INTO users VALUES (?, ?, ?)', (username, password, admin))
        conn.commit()
        conn.close()
        
        return redirect(url_for('login'))
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('db/users.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            session['username'] = user[0]
            return redirect(url_for('main'))
        else:
            return render_template('login.html', error=True)
    else:
        return render_template('login.html', error=False)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/robots.txt')
def robots():
    text = '''Allow:
        /register
        /login
        /'''
    return text,200

@app.route('/')
def main():
    if 'username' in session:

        username = session['username']
        conn = sqlite3.connect('db/users.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()
        if user[2] == 'c4ca4238a0b923820dcc509a6f75849b':
            return render_template('main.html', username=username, flag='You look like an admin:\n'+FLAG)
        
        return render_template('main.html', username=username, flag='You aren\'t the admin...')

    return redirect(url_for('login'))


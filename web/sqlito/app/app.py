from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    with open(__file__, "r") as f:
        source_code = f.read()
    return source_code, 200, {'Content-Type': 'text/plain'}


@app.route('/login', methods=['GET'])
def login_form():
    return '''
    <form method="POST" action="/login">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username">
        <br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password">
        <br>
        <input type="submit" value="Submit">
    </form>
    '''

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = '{}' AND password = '{}'".format(username, password))
    user = c.fetchone()
    conn.close()
    if user:
        with open('flag.txt', "r") as f:
            flag = f.read()
        return f'Welcome\n{flag}', 200, {'Content-Type': 'text/plain'}
    else:
        return "Invalid username or password"

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=6001)

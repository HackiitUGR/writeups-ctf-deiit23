#!/bin/bash

cd /app
DB_FILE="database.db"

# init database
python3 << EOF
import sqlite3

# Open a connection to the database
conn = sqlite3.connect('$DB_FILE')

# Create the users table
conn.execute('''CREATE TABLE users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             username TEXT NOT NULL,
             password TEXT NOT NULL);''')

# Insert the admin user into the users table
conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', '3666cbad3adc75e1b47c8e97d78b0970'))

# Commit the changes and close the connection
conn.commit()
conn.close()
EOF

# run flask app
python3 app.py
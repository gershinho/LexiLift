from flask import Flask
import sqlite3
from app import *



def user_db():
    with sqlite3.connect('user.db') as con:
        cursor = con.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL, 
                name TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logins (
                user_id INTEGER,
                login_count INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS points (
                user_id INTEGER,
                points INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        con.commit()

def increment_login_count(user_id):
    con = sqlite3.connect("user.db")
    c = con.cursor()
    
    c.execute("SELECT login_count FROM logins WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    
    if result:
        c.execute("UPDATE logins SET login_count = login_count + 1 WHERE user_id = ?", (user_id,))
    else:
        c.execute("INSERT INTO logins (user_id, login_count) VALUES (?, ?)", (user_id, 1))
    
    con.commit()
    con.close()

def insertUser(email, name, psw):
    con = sqlite3.connect("user.db")
    c = con.cursor()
    c.execute("INSERT INTO users (email, name, password) VALUES (?, ?, ?)", (email, name, psw))
    con.commit()
    con.close()

def fetch_users():
    con = sqlite3.connect("user.db")
    c = con.cursor()
    c.execute("SELECT id, email, password, name FROM users")
    users = c.fetchall()
    con.close()
    return users

def find_user(email, psw):
    con = sqlite3.connect("user.db")
    c = con.cursor()
    c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, psw))
    user = c.fetchone()
    con.close()
    print(user)
    return user

def clear_data():
    ...
    
def get_user_by_email(email):
    con = sqlite3.connect("user.db")
    c = con.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    con.close()
    return user

def check_user_exist(email, psw):
    con = sqlite3.connect("user.db")
    c = con.cursor()
    c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, psw))
    user = c.fetchone()
    con.close()
    return user



def update_points(user_id, points_change):
    con = sqlite3.connect("user.db")
    cursor = con.cursor()

    # Fetch current points
    cursor.execute('SELECT points FROM points WHERE user_id = ?', (user_id,))
    current_points = cursor.fetchone()

    if current_points:
        new_points = current_points[0] + points_change
        cursor.execute('UPDATE points SET points = ? WHERE user_id = ?', (new_points, user_id))
    else:
        cursor.execute('INSERT INTO points (user_id, points) VALUES (?, ?)', (user_id, points_change))

    con.commit()
    con.close()

def get_user_points(user_id):
    con = sqlite3.connect("user.db")
    cursor = con.cursor()

    # Fetch current points
    cursor.execute('SELECT points FROM points WHERE user_id = ?', (user_id,))
    points = cursor.fetchone()

    con.close()

    return points[0] if points else 0

user_db()
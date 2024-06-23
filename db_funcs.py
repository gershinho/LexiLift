import sqlite3

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
                level TEXT DEFAULT 'easy',
                correct_count INTEGER DEFAULT 0,
               
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        con.commit()

        # Print the database schema for the points table
        

def check_user_exist(email, psw):
    con = sqlite3.connect("user.db")
    c = con.cursor()
    c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, psw))
    user = c.fetchone()
    con.close()
    return user

def find_user(email, psw):
    con = sqlite3.connect("user.db")
    c = con.cursor()
    c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, psw))
    user = c.fetchone()
    con.close()
    return user

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

def update_points(user_id, points_change):
    con = sqlite3.connect("user.db")
    cursor = con.cursor()

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
    cursor.execute('SELECT points FROM points WHERE user_id = ?', (user_id,))
    points = cursor.fetchone()
    con.close()
    return points[0] if points else 0

def get_user_correc(user_id):
    con = sqlite3.connect("user.db")
    cursor = con.cursor()
    cursor.execute('SELECT correct_count FROM points WHERE user_id = ?', (user_id,))
    count = cursor.fetchone()
    con.close()
    return count[0] if count else 0

def get_user_lvl(user_id):
    con = sqlite3.connect("user.db")
    cursor = con.cursor()
    cursor.execute('SELECT level FROM points WHERE user_id = ?', (user_id,))
    lvl = cursor.fetchone()
    con.close()
    return lvl[0] if lvl else 'easy'

def get_user_num(user_id):
    con = sqlite3.connect("user.db")
    cursor = con.cursor()
    cursor.execute('SELECT num FROM points WHERE user_id = ?', (user_id,))
    num = cursor.fetchone()
    con.close()
    return num[0] if num else 1

def update_count(user_id, count_change):
    con = sqlite3.connect("user.db")
    cursor = con.cursor()
    cursor.execute('SELECT correct_count FROM points WHERE user_id = ?', (user_id,))
    current_count = cursor.fetchone()

    if current_count:
        new_count = count_change
        cursor.execute('UPDATE points SET correct_count = ? WHERE user_id = ?', (new_count, user_id))
    else:
        cursor.execute('INSERT INTO points (user_id, correct_count) VALUES (?, ?)', (user_id, count_change))

    con.commit()
    con.close()

def update_level(user_id, level):
    con = sqlite3.connect("user.db")
    cursor = con.cursor()
    cursor.execute('SELECT level FROM points WHERE user_id = ?', (user_id,))
    current_level = cursor.fetchone()
    
    print(f"Updating level for user_id {user_id} to {level}")  # Debug print statement

    if current_level:
        cursor.execute('UPDATE points SET level = ? WHERE user_id = ?', (level, user_id))
    else:
        cursor.execute('INSERT INTO points (user_id, level) VALUES (?, ?)', (user_id, level))

    con.commit()
    con.close()

def update_num(user_id, num):
    con = sqlite3.connect("user.db")
    cursor = con.cursor()
    cursor.execute('SELECT num FROM points WHERE user_id = ?', (user_id,))
    current_num = cursor.fetchone()

    if current_num:
        cursor.execute('UPDATE points SET num = ? WHERE user_id = ?', (num, user_id))
    else:
        cursor.execute('INSERT INTO points (user_id, num) VALUES (?, ?)', (user_id, num))

    con.commit()
    con.close()

user_db()
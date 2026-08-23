import sqlite3 
DB_NAME = "oto.db"

def connect_db():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(""" CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, name TEXT, interface_language TEXT)""")

    cursor.execute(""" CREATE TABLE IF NOT EXISTS learning_languages (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, language TEXT NOT NULL, active INTEGER NOT NULL DEFAULT 1, UNIQUE(user_id, language), FOREIGN KEY(user_id) REFERENCES users(user_id))""")

    conn.commit()
    conn.close()

def save_user( user_id, name, interface_language): 
        conn = connect_db()
        cursor = conn.cursor() 

        cursor.execute(""" INSERT OR REPLACE INTO users (user_id, name, interface_language)
        VALUES (?, ?, ?) """, (user_id, name, interface_language)) 

        conn.commit()
        conn.close()

def add_learning_language(user_id, language):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""UPDATE learning_languages SET active = 0 WHERE user_id = ? """, (user_id,))


    cursor.execute("""INSERT INTO learning_languages (user_id, language, active) VALUES (?, ?, 1) ON CONFLICT(user_id, language) DO UPDATE SET active = 1""", (user_id, language))
    conn.commit()
    conn.close()

def get_user(user_id): 
    conn = connect_db()
    cursor = conn.cursor()
      
    cursor.execute("""SELECT user_id, name,interface_language FROM users WHERE user_id = ?""", (user_id,)) 
    user = cursor.fetchone()
    conn.close()
    return user 

def get_active_language(user_id):  

     conn = connect_db()
     cursor = conn.cursor()

     cursor.execute("""SELECT language FROM learning_languages WHERE user_id = ? AND active = 1 LIMIT 1""", (user_id,))

     language = cursor.fetchone()
     conn.close()
     return language[0] if language else None

def update_name(user_id, name):
     conn= connect_db()
     cursor = conn.cursor()
     cursor.execute("""UPDATE users SET name = ? WHERE user_id = ?""",
                     (name, user_id))
     conn.commit()
     conn.close()

def update_interface_language(user_id, language):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""UPDATE users SET interface_language = ? WHERE user_id = ?""",
                        (language, user_id))
        conn.commit()
        conn.close()

def get_learning_languages(user_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, language, active
        FROM learning_languages
        WHERE user_id = ?
    """, (user_id,))

    languages = cursor.fetchall()

    conn.close()

    return languages      





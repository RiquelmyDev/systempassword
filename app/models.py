import sqlite3

def create_connection():
    return sqlite3.connect('passwords.db')

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    # Tabela de usuários
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL)''')

    # Tabela de emails e senhas
    cursor.execute('''CREATE TABLE IF NOT EXISTS emails (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        email_type TEXT NOT NULL,
                        email_address TEXT NOT NULL,
                        password TEXT NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users(id))''')

    conn.commit()
    conn.close()

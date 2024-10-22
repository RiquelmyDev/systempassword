import sqlite3

DATABASE = 'database/passwords.db'  # Caminho para o banco de dados

# Função para criar uma conexão com o banco de dados
def create_connection():
    try:
        conn = sqlite3.connect(DATABASE)  # Conecta ao banco de dados
        conn.row_factory = sqlite3.Row  # Permite acessar as colunas pelo nome
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para criar as tabelas necessárias
def create_tables():
    conn = create_connection()
    if conn:  # Verifica se a conexão foi estabelecida
        cursor = conn.cursor()
        
        # Criação da tabela users
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')

        # Criação da tabela emails
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                email_type TEXT NOT NULL,
                email_address TEXT NOT NULL,
                password TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')

        conn.commit()
        conn.close()  # Fecha a conexão após criar as tabelas

# Função para criar um novo usuário
def create_user(username, password):
    conn = create_connection()
    if conn:  # Verifica se a conexão foi estabelecida
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()  # Fecha a conexão após a inserção

# Função para obter um usuário pelo nome de usuário
def get_user_by_username(username):
    conn = create_connection()
    if conn:  # Verifica se a conexão foi estabelecida
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()  # Obtém o usuário encontrado
        conn.close()  # Fecha a conexão após a consulta
        return user
    return None

# Função para adicionar um novo email
def add_email(user_id, email_type, email_address, password):
    conn = create_connection()
    if conn:  # Verifica se a conexão foi estabelecida
        cursor = conn.cursor()
        cursor.execute("INSERT INTO emails (user_id, email_type, email_address, password) VALUES (?, ?, ?, ?)", 
                       (user_id, email_type, email_address, password))
        conn.commit()
        conn.close()  # Fecha a conexão após a inserção

# Função para obter os emails de um usuário
def get_emails_by_user_id(user_id):
    conn = create_connection()
    if conn:  # Verifica se a conexão foi estabelecida
        cursor = conn.cursor()
        cursor.execute('''SELECT email_type, email_address, password FROM emails WHERE user_id = ?''', (user_id,))
        emails = cursor.fetchall()  # Obtém todos os resultados da consulta
        conn.close()  # Fecha a conexão
        return emails  # Retorna uma lista de tuplas com (tipo, email, senha)
    return []

# Função para criar as tabelas (chamada inicial)
def initialize_database():
    create_tables()  # Chama a função para criar as tabelas


"""import sqlite3

DATABASE = 'database/passwords.db' # Caminho para o banco de dados

import sqlite3

def create_tables():
    conn = sqlite3.connect('database/passwords.db')  # Caminho correto para o seu banco de dados
    cursor = conn.cursor()
    
    # Criação da tabela users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Criação da tabela passwords (ou como você nomeou)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            email_type TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()



# Função para criar uma conexão com o banco de dados
def create_connection():
    try:
        conn = sqlite3.connect(DATABASE) # Conecta ao banco de dados
        conn.row_factory = sqlite3.Row # Permite acessar as colunas pelo nome
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para criar a tabela de usuários
def create_users_table():
    conn = create_connection()
    if conn:  # Verifica se a conexão foi estabelecida
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL)''')
        conn.commit()
        conn.close()  # Fecha a conexão após criar a tabela

# Função para criar tabela de emails
def create_emails_table():
    conn = create_connection()
    if conn:  # Verifica se a conexão foi estabelecida
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS emails (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER,
                            email_type TEXT,
                            email_address TEXT,
                            password TEXT,
                            FOREIGN KEY (user_id) REFERENCES users (id))''')
        conn.commit()
        conn.close()  # Fecha a conexão após criar a tabela
                       
# Função para criar um novo usuário
def create_user(username, password):
    conn = create_connection()
    if conn:  # Verifica se a conexão foi estabelecida
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()  # Fecha a conexão após a inserção


# Função para obter um usuário pelo nome de usuário
def get_user_by_username(username):
    conn = create_connection()
    if conn:  # Verifica se a conexão foi estabelecida
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()  # Obtém o usuário encontrado
        conn.close()  # Fecha a conexão após a consulta
        return user
    return None

# Função para adicionar um novo email
def add_email(user_id, email_type, email_address, password):
    conn = create_connection()
    if conn:  # Verifica se a conexão foi estabelecida
        cursor = conn.cursor()
        cursor.execute("INSERT INTO emails (user_id, email_type, email_address, password) VALUES (?, ?, ?, ?)", 
                       (email_type, email_address, password, user_id))
        conn.commit()
        conn.close()  # Fecha a conexão após a inserção

# Função para obter os emails de um usuário
def get_emails_by_user_id(user_id):
    conn = create_connection()
    if conn:  # Verifica se a conexão foi estabelecida
        cursor = conn.cursor()
        cursor.execute('''SELECT email_type, email, password FROM emails WHERE user_id = ?''', (user_id,))
        emails = cursor.fetchall()  # Obtém todos os resultados da consulta
        conn.close()
        return emails  # Retorna uma lista de tuplas com (tipo, email, senha)
    return []"""
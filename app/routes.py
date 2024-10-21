from flask import Flask, render_template, request, redirect, session
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Conexão com o banco de dados
def create_connection():
    return sqlite3.connect('database/passwords.db')  # Alterando para a pasta 'database'

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'),user[2]):
            session['user_id'] = user[0] # Armazenar ID do usuário na sessão
            return redirect('/dashboard')
        else:
            return 'Login ou senha inválidos'
        
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
            conn.commit()
        except sqlite3.IntegrityError:
            return 'O nome de usuário já existe'

        return redirect('/login')
    
    return render_template('register.html')
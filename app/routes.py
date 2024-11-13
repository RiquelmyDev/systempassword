from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import create_user, get_user_by_username, add_email, get_emails_by_user_id
from functools import wraps

# Criação do Blueprint para as rotas
bp = Blueprint('main', __name__)

# Decorador para proteger as rotas que requerem login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa estar logado para acessar essa página.')
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

# Rota para o registro de novos usuários
@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    User Registration
    ---
    tags:
      - User
    parameters:
      - name: username
        in: formData
        type: string
        required: true
        description: Username for the new user
      - name: password
        in: formData
        type: string
        required: true
        description: Password for the new user
    responses:
      200:
        description: User registered successfully
      400:
        description: Invalid input
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        create_user(username, hashed_password)
        flash('Usuário registrado com sucesso! Faça login para continuar.')
        return redirect(url_for('main.login'))
    return render_template('register.html')

# Rota para login de usuários
@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    User Login
    ---
    tags:
      - User
    parameters:
      - name: username
        in: formData
        type: string
        required: true
        description: Username of the user
      - name: password
        in: formData
        type: string
        required: true
        description: Password of the user
    responses:
      200:
        description: Login successful
      401:
        description: Unauthorized (invalid username or password)
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            flash('Login bem-sucedido!')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Usuário ou senha inválidos.')
    return render_template('login.html')

# Rota para o dashboard (página inicial após login)
@bp.route('/dashboard')
@login_required
def dashboard():
    """
    Dashboard
    ---
    tags:
      - User
    responses:
      200:
        description: Dashboard page for authenticated users
      401:
        description: Unauthorized
    """
    return render_template('dashboard.html')

# Rota para adicionar um novo email
@bp.route('/manage_passwords', methods=['GET', 'POST'])
@login_required
def manage_passwords():
    """
    Manage Passwords
    ---
    tags:
      - Email
    parameters:
      - name: email_type
        in: formData
        type: string
        required: true
        description: Type of email (e.g., Personal, Work)
      - name: email_address
        in: formData
        type: string
        required: true
        description: Email address
      - name: password
        in: formData
        type: string
        required: true
        description: Password for the email
    responses:
      200:
        description: Email added successfully
      400:
        description: Invalid input
    """
    if request.method == 'POST':
        email_type = request.form['email_type']
        email_address = request.form['email_address']
        password = request.form['password']
        user_id = session['user_id']
        add_email(user_id, email_type, email_address, password)
        flash('Email adicionado com sucesso!')
        return redirect(url_for('main.manage_passwords'))
    return render_template('manage_passwords.html')

# Rota para visualizar os emails salvos
@bp.route('/view_passwords', methods=['GET'])
@login_required
def view_passwords():
    """
    View Saved Emails
    ---
    tags:
      - Email
    responses:
      200:
        description: List of saved emails
      401:
        description: Unauthorized
    """
    user_id = session['user_id']
    emails = get_emails_by_user_id(user_id)
    if not emails:
        flash('Você ainda não salvou nenhum email.')
    return render_template('view_passwords.html', emails=emails)

# Rota para logout
@bp.route('/logout')
@login_required
def logout():
    """
    User Logout
    ---
    tags:
      - User
    responses:
      200:
        description: Logout successful
      401:
        description: Unauthorized
    """
    session.clear()
    flash('Você foi desconectado com sucesso.')
    return redirect(url_for('main.login'))



"""from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import create_user, get_user_by_username, add_email, get_emails_by_user_id, create_users_table, create_emails_table
from functools import wraps

# Criação do Blueprint para as rotas
bp = Blueprint('main', __name__)

# Decorador para proteger as rotas que requerem login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa estar logado para acessar essa página.')
            return redirect(url_for('main.login'))  # Altere para 'main.login'
        return f(*args, **kwargs)
    return decorated_function

# Rota para o registro de novos usuários
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Gera o hash da senha
        hashed_password = generate_password_hash(password)

        # Cria um novo usuário no banco de dados
        create_user(username, hashed_password)
        flash('Usuário registrado com sucesso! Faça login para continuar.')
        return redirect(url_for('main.login'))  # Altere para 'main.login'      
    return render_template('register.html')

# Rota para login de usuários
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Busca o usuário no banco de dados
        user = get_user_by_username(username)

        # Verifica se o usuário existe e se a senha está correta
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']  # Armazena o ID do usuário na sessão
            flash('Login bem-sucedido!')
            return redirect(url_for('main.dashboard'))  # Altere para 'main.dashboard'
        else:
            flash('Usuário ou senha inválidos.')

    return render_template('login.html') 

# Rota para o dashboard (página inicial após login)
@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')  # Corrigido para 'dashboard.html'

# Rota para adicionar um novo email
@bp.route('/manage_passwords', methods=['GET', 'POST'])
@login_required
def manage_passwords():
    if request.method == 'POST':
        email_type = request.form['email_type']
        email_address = request.form['email_address']
        password = request.form['password']
        user_id = session['user_id']  # Obtém o ID do usuário da sessão

        # Adiciona o novo email ao banco de dados
        add_email(email_type, email_address, password, user_id)
        flash('Email adicionado com sucesso!')
        return redirect(url_for('main.manage_passwords'))  # Altere para 'main.manage_passwords'

    return render_template('manage_passwords.html')

# Rota para visualizar os emails salvos
@bp.route('/view_passwords', methods=['GET'])
@login_required
def view_passwords():
  user_id = session['user_id']  # Obtém o ID do usuário logado
  emails = get_emails_by_user_id(user_id)  # Obtém os emails do usuário

  # Verifica se a consulta retornou algum resultado
  if not emails:
      flash('Você ainda não salvou nenhum email.')
  return render_template('view_passwords.html', emails=emails)

# Rota para logout
@bp.route('/logout')
@login_required
def logout():
    session.clear()  # Limpa a sessão
    flash('Você foi desconectado com sucesso.')
    return redirect(url_for('main.login'))  # Altere para 'main.login'"""


#ISSO DAQUI VAI SERVIR SO PRA ATUALIZAR MEU GITHUB kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk"""
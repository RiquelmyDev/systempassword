from flask import Flask
import os

# Função para criar a aplicação Flask
def create_app():
    app = Flask(__name__)

    # Definir a chave secreta da aplicação para uso em sessões
    app.secret_key = os.getenv('SECRET_KEY', 'sua_chave_secreta')

    # Configuração do banco de dados (se necessário, pode adicionar mais configurações)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/passwords.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Registrar as rotas (importa o arquivo de rotas e registra no app)
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
from app import create_app
from flasgger import Swagger
from flask import Flask

app = Flask(__name__)
swagger = Swagger(app)


app = create_app()  # Chamando a função para criar a aplicação

if __name__ == "__main__":
    app.run(debug=True)

from app import create_app

app = create_app()  # Chamando a função para criar a aplicação

if __name__ == "__main__":
    app.run(debug=True)

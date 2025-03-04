from app import create_app
from app.database import init_db

app = create_app()

if __name__ == "__main__":
    init_db()  # Cria o banco se não existir
    app.run(debug=False, host='0.0.0.0', port=4000)

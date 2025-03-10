from flask_cors import CORS
from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Habilitar CORS para todos os métodos
    CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE"]}})
    
    app.config["DATABASE"] = "instance/database.sqlite"

    from app.routes import init_routes
    init_routes(app)

    return app

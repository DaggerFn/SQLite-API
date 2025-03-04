from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config["DATABASE"] = "instance/meu_banco.sqlite"

    from app.routes import init_routes
    init_routes(app)

    return app

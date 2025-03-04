from flask import request, jsonify
from app.database import get_db

def init_routes(app):
    @app.route("/materiais", methods=["GET"])
    def get_materiais():
        conn = get_db()
        materiais = conn.execute("SELECT * FROM materiais").fetchall()
        return jsonify([dict(row) for row in materiais])

    @app.route("/materiais", methods=["POST"])
    def create_material():
        data = request.get_json()
        conn = get_db()
        cursor = conn.execute(
            "INSERT INTO materiais (id_material, locale_material, description_material) VALUES (?, ?, ?)",
            (data["id_material"], data["locale_material"], data["description_material"])
        )
        conn.commit()
        return jsonify({"id_material": data["id_material"], "message": "Material inserido com sucesso!"}), 201

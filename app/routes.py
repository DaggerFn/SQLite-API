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
        # Rota para deletar um material pelo ID
    
    @app.route("/materiais/<id_material>", methods=["DELETE"])
    def delete_material(id_material):
        conn = get_db()
        cursor = conn.execute("DELETE FROM materiais WHERE id_material = ?", (id_material,))
        conn.commit()
        
        # Verifica se alguma linha foi afetada
        if cursor.rowcount == 0:
            return jsonify({"error": "Material não encontrado"}), 404
        
        return jsonify({"message": "Material deletado com sucesso!"}), 200
    
    @app.route("/materiais/<id_material>", methods=["PUT"])
    def update_material(id_material):
        data = request.get_json()  # Obtém os dados enviados no JSON
        conn = get_db()

        # Verifica se o material existe antes de tentar atualizar
        cursor = conn.execute("SELECT * FROM materiais WHERE id_material = ?", (id_material,))
        material = cursor.fetchone()
        
        if not material:
            return jsonify({"error": "Material não encontrado"}), 404

        # Atualiza os dados no banco de dados
        conn.execute(
            "UPDATE materiais SET locale_material = ?, description_material = ? WHERE id_material = ?",
            (data["locale_material"], data["description_material"], id_material)
        )
        conn.commit()

        return jsonify({"message": "Material atualizado com sucesso!"}), 200
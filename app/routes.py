from flask import request, jsonify
from app.database import get_db
from datetime import datetime


def init_routes(app):
    @app.route("/materiais", methods=["GET"])
    def get_materiais():
        conn = get_db()
        materiais = conn.execute("SELECT * FROM tabel_materials").fetchall()
        return jsonify([dict(row) for row in materiais])

    @app.route("/materiais", methods=["POST"])
    def create_material():
        data = request.get_json()
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # print(now_str,' < tipo de var > ', type(now_str))
        
        if not data:
            return jsonify({"error": "Nenhum dado enviado"}), 400

        conn = get_db()
        cursor = conn.execute(
            "INSERT INTO tabel_materials (id_material, locale_material, quantidade, description_material, last_mod) VALUES (?, ?, ?, ?, ?)",
            (data["id_material"], data["locale_material"], data["quantidade"], data["description_material"], now_str)
            
        )
        conn.commit()

        return jsonify({"message": "Material inserido com sucesso!"}), 201

    
    @app.route("/materiais/<id_material>", methods=["DELETE"])
    def delete_material(id_material):
        conn = get_db()
        cursor = conn.execute("DELETE FROM tabel_materials WHERE id_material = ?", (id_material,))
        conn.commit()
        
        # Verifica se alguma linha foi afetada
        if cursor.rowcount == 0:
            return jsonify({"error": "Material não encontrado"}), 404
        
        return jsonify({"message": "Material deletado com sucesso!"}), 200
    
    @app.route("/materiais/<id_material>", methods=["PUT"])
    def update_material(id_material):
        data = request.get_json()  # Obtém os dados enviados no JSON
        conn = get_db()
        now_str_for_put = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        

        # Verifica se o material existe antes de tentar atualizar
        cursor = conn.execute("SELECT * FROM tabel_materials WHERE id_material = ?", (id_material,))
        material = cursor.fetchone()
        
        if not material:
            return jsonify({"error": "Material não encontrado"}), 404

        # Atualiza os dados no banco de dados
        conn.execute(
            "UPDATE tabel_materials SET locale_material = ?, quantidade = ?, description_material = ? , last_mod = ?, id_material = ?",
            (data["locale_material"], data["quantidade"], data["description_material"],now_str_for_put, id_material)
        )
        conn.commit()

        return jsonify({"message": "Material atualizado com sucesso!"}), 200
    
    
    @app.route("/materiais/<id_material>", methods=["GET"])
    def searchGet(id_material):
        conn = get_db()
        
        cursor = conn.execute("SELECT * FROM tabel_materials WHERE id_material = ?", (id_material,))
        material = cursor.fetchone()
        
        if not material:
            return jsonify({"error": "Material não encontrado"}), 404
        
        '''
        for row in material:
            print(row)

        print(dict(material))
        '''
        return jsonify([dict(material)])
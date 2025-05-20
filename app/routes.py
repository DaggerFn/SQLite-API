from flask import request, jsonify
from app.database import get_db
from datetime import datetime
import requests


def init_routes(app):
    # Busca Materiais
    @app.route("/materiais", methods=["GET"])
    def get_materiais():
        conn = get_db()
        # # Remove todos os materiais com quantidade igual a 0
        conn.execute("DELETE FROM tabel_materials WHERE quantidade = 0")
        conn.commit()
        # Busca todos os materiais restantes
        materiais = conn.execute("SELECT * FROM tabel_materials").fetchall()
        return jsonify([dict(row) for row in materiais])

    # Cria/Registra o material
    @app.route("/materiais", methods=["POST"])
    def create_material():
        data = request.get_json()
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # print(now_str,' < tipo de var > ', type(now_str))
        
        if not data:
            return jsonify({"error": "Nenhum dado enviado"}), 400

        get_description(data)


        conn = get_db()
        cursor = conn.execute(
            "INSERT INTO tabel_materials (id_material, locale_material, quantidade, description_material, last_mod) VALUES (?, ?, ?, ?, ?)",
            (data["id_material"], data["locale_material"], data["quantidade"], data["description_material"], now_str)
            
        )


        conn.commit()

        return jsonify({"message": "Material inserido com sucesso!"}), 201

    # Deleta o material
    @app.route("/materiais/<id_material>", methods=["DELETE"])
    def delete_material(id_material):
        conn = get_db()
        cursor = conn.execute("DELETE FROM tabel_materials WHERE id_material = ?", (id_material,))
        conn.commit()
        
        # Verifica se alguma linha foi afetada
        if cursor.rowcount == 0:
            return jsonify({"error": "Material não encontrado"}), 404
        
        return jsonify({"message": "Material deletado com sucesso!"}), 200
    
    # Atualiza o material
    @app.route("/materiais/<int:id_material>", methods=["PUT"])
    def update_material(id_material):
        data = request.get_json()
        conn = get_db()
        now_str_for_put = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Verifica se existe
        cursor = conn.execute(
            "SELECT 1 FROM tabel_materials WHERE id_material = ?",
            (id_material,)
        )
        if cursor.fetchone() is None:
            return jsonify({"error": "Material não encontrado"}), 404

        # Atualiza somente a linha cujo id_material bate
        conn.execute(
            """
            UPDATE tabel_materials
            SET locale_material     = ?,
                quantidade          = ?,
                description_material= ?,
                last_mod            = ?
            WHERE id_material        = ?
            """,
            (
                data["locale_material"],
                data["quantidade"],
                data["description_material"],
                now_str_for_put,
                id_material
            )
        )
        conn.commit()

        return jsonify({"message": "Material atualizado com sucesso!"}), 200

    # Busca o material específico
    @app.route("/materiais/<id_material>", methods=["GET"])
    def searchGet(id_material):
        conn = get_db()
        
        cursor = conn.execute("SELECT * FROM tabel_materials WHERE id_material = ?", (id_material,))
        material = cursor.fetchone()
        
        if not material:
            return jsonify({"error": "Material não encontrado"}), 404
        
        '''
        # mock de data e visualização dos dados
        for row in material:
            print(row)

        print(dict(material))
        
        
        data = {'id': 1001,
                 'id_material': 11146098, 
                 'locale_material': '02-13-05', 
                 'quantidade': 10, 
                 'description_material': 'Z', 
                 'last_mod': '2025-05-16 08:17:00'}
        
        print(material["quantidade"])
        '''
        
        if material["quantidade"] == 0:
            conn.execute("DELETE FROM tabel_materials WHERE quantidade = 0")
            conn.commit()

            return jsonify({"error": "Material indisponível no Estoque"}), 404
        
        return jsonify([dict(material)])
    
    
    
    def get_description(data):


        # api_link_description = f"http://127.0.0.1:4000/completo/{data["id_material"]}"
        
        
        api_link_description = f"http://127.0.0.1:6000/test"
        
        '''Mock of api response
        
        {
        "ClassList": {
            "Class": {
            "CharacteristicList": {
                "Characteristic": {
                "DataType": null,
                "Name": "ZPESO_CALCULADO_01",
                "Value": "00001",
                "ValueDescription": {
                    "#text": "SIM",
                    "@language": "PT"
                }
                }
            },
            "Name": "MAT_ADM_MOTOR"
            }
        },
        "ClassType": "001",
        "MaterialDescription": "MOTOR 5.5kW 4P 132S WFF2", <----- description,(i need get this value and pass for data["description_material"])
        "MaterialNumber": "17329732",
        "ValidFrom": "2025-05-17"
        }
        
        '''
        
        try:

            flask_response = requests.get(api_link_description)
        
            if flask_response.status_code == 404:
                # Se a API retornar 404, defina um valor padrão
                data["description_material"] = "Sem descrição"
                print("API retornou 404 - Definindo descrição padrão.")
        
        
            if "description_material" not in data or data["description_material"] is '':
                # Se não houver descrição, defina um valorr padrão
                # data["description_material"] = "Sem descrição"

                # Verifica se a resposta da API foi bem-sucedida
                if flask_response.status_code == 200:
                    # Converte a resposta JSON em um dicionário
                    response_data = flask_response.json()
                    
                    # Acessa o valor desejado
                    data["description_material"] = response_data["MaterialDescription"]
                else:
                    # Se a API não retornar sucesso, defina um valor padrão
                    data["description_material"] = "Sem descrição"
            
            
            print(dict(data))

        except KeyError as e:
            # Se a chave não existir, defina um valor padrão
            data["description_material"] = "Sem descrição"
            print(f"KeyError: {e} - Definindo descrição padrão.")
        
        return data
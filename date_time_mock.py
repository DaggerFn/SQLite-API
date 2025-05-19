import sqlite3
import random
from datetime import datetime, timedelta

# Caminho para o arquivo SQLite
db_path = 'instance/teste.sqlite'

# Conectar ao banco de dados
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Buscar todos os rowids da tabela
cursor.execute("SELECT rowid FROM tabel_materials ORDER BY rowid")
rows = cursor.fetchall()

# Data inicial e data máxima
base_date = datetime(2025, 1, 1, 0, 0, 0)
max_date = datetime(2025, 1, 12, 0, 0, 0)

# Atualizar cada linha
for idx, (rowid,) in enumerate(rows):
    # Calcula a data, incrementando um dia a cada linha
    new_date = base_date + timedelta(days=idx)
    # Se a data ultrapassar a data máxima, ajusta para a data máxima
    if new_date > max_date:
        new_date = max_date
    # Gera hora aleatória (minutos e segundos zerados)
    hour = random.randint(0, 23)
    new_date = new_date.replace(hour=hour, minute=0, second=0)
    # Atualiza o registro
    cursor.execute(
        "UPDATE tabel_materials SET last_mod = ? WHERE rowid = ?",
        (new_date.strftime("%Y-%m-%d %H:%M:%S"), rowid)
    )

# Salvar alterações e fechar conexão
conn.commit()
conn.close()

print("Atualização de last_mod concluída com sucesso!")

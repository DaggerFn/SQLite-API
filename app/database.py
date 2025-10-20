import sqlite3

DB_PATH = "instance/database.sqlite"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Retorna resultados como dicionários
    return conn

def init_db():
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS tabel_materials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_material TEXT NOT NULL,
                locale_material TEXT NxOT NULL,
                quantidade FLOAT NOT NULL,
                description_material TEXT NOT NULL,
                last_mod DATETIME NOT NULL
            );
        """)
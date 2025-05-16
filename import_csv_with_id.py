#!/usr/bin/env python3
import csv
import sqlite3
import os

def csv_to_sqlite_with_id(csv_path, sqlite_path, table_name):
    # Abre (ou cria) o banco SQLite
    conn = sqlite3.connect(sqlite_path)
    cur = conn.cursor()

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)  # pega a primeira linha como cabeçalhos

        # Monta a definição de colunas (sem o ID)
        cols_defs = ', '.join(f'"{h}" TEXT' for h in headers)

        # 1) Cria a nova tabela com id autoincrement
        cur.execute(f'''
            CREATE TABLE IF NOT EXISTS "{table_name}" (
              id   INTEGER PRIMARY KEY AUTOINCREMENT,
              {cols_defs}
            );
        ''')

        # 2) Prepara o INSERT (sem a coluna id, que é gerada automaticamente)
        placeholders = ', '.join('?' for _ in headers)
        insert_sql = f'INSERT INTO "{table_name}" ({", ".join(f"""{h}""" for h in headers)}) VALUES ({placeholders});'

        # 3) Insere linha a linha
        for row in reader:
            cur.execute(insert_sql, row)

    conn.commit()
    conn.close()
    print(f'Importação concluída: tabela "{table_name}" em "{sqlite_path}", com coluna id autoincrement.')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Importa um CSV para SQLite criando PK autoincrement'
    )
    parser.add_argument(
        'csv_file',
        help='Caminho para o arquivo CSV de entrada (ex: MOCK_DATA.csv)'
    )
    parser.add_argument(
        'sqlite_file',
        help='Caminho para o arquivo SQLite de saída (ex: meu_banco.sqlite)'
    )
    parser.add_argument(
        '--table', '-t',
        default='my_table',
        help='Nome da tabela a criar (padrão: my_table)'
    )
    args = parser.parse_args()

    # Garante que a pasta destino existe
    os.makedirs(os.path.dirname(os.path.abspath(args.sqlite_file)), exist_ok=True)

    csv_to_sqlite_with_id(args.csv_file, args.sqlite_file, args.table)

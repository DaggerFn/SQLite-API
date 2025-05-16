#!/usr/bin/env python3
import csv
import sqlite3
import argparse
import os

def csv_to_sqlite(csv_path, sqlite_path, table_name):
    # Abre conexão com o SQLite (cria o arquivo se não existir)
    conn = sqlite3.connect(sqlite_path)
    cur = conn.cursor()

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)  # lê cabeçalhos da primeira linha

        # Cria tabela com todas as colunas como TEXT
        cols = ', '.join([f'"{h}" TEXT' for h in headers])
        cur.execute(f'CREATE TABLE IF NOT EXISTS "{table_name}" ({cols});')

        # Prepara comando de inserção
        placeholders = ', '.join(['?'] * len(headers))
        insert_sql = f'INSERT INTO "{table_name}" VALUES ({placeholders});'

        # Insere cada linha do CSV
        for row in reader:
            cur.execute(insert_sql, row)

    conn.commit()
    conn.close()
    print(f'Tabela "{table_name}" criada em {sqlite_path} com sucesso.')

def main():
    parser = argparse.ArgumentParser(
        description='Importa um CSV para um banco de dados SQLite.'
    )
    parser.add_argument('csv_file', help='Caminho para o arquivo .csv de entrada')
    parser.add_argument('sqlite_file', help='Caminho para o arquivo .sqlite de saída')
    parser.add_argument('--table', '-t', default='csv_data',
                        help='Nome da tabela a ser criada (padrão: csv_data)')
    args = parser.parse_args()

    # Certifica-se de que o diretório do SQLite existe
    os.makedirs(os.path.dirname(os.path.abspath(args.sqlite_file)), exist_ok=True)

    csv_to_sqlite(args.csv_file, args.sqlite_file, args.table)

if __name__ == '__main__':
    main()

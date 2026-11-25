import os
import mysql.connector
from mysql.connector import Error


def conectar():
    try:
        conexao = mysql.connector.connect(
            host=os.getenv("DB_HOST", "127.0.0.1"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME", "monitoramento_processos")
        )

        if conexao.is_connected():
            return conexao

    except Error as erro:
        print(f"Erro ao conectar ao MySQL: {erro}")

    return None

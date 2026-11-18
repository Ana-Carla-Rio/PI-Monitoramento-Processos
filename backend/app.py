
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from pathlib import Path
from database import conectar

app = Flask(__name__)
CORS(app)

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


@app.route("/", methods=["GET"])
def inicio():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/cadProcessos", methods=["GET"])
def tela_processos():
    return send_from_directory(FRONTEND_DIR, "cadProcessos.html")


@app.route("/api/processos", methods=["GET"])
def listar_processos():
    conexao = conectar()

    if conexao is None:
        return jsonify({"erro": "Não foi possível conectar ao banco de dados"}), 500

    cursor = None

    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, nome, tipo, setor, data_criacao
            FROM processos
            ORDER BY id DESC
        """)

        processos = cursor.fetchall()

        for processo in processos:
            if processo["data_criacao"]:
                processo["data_criacao"] = processo["data_criacao"].isoformat()

        return jsonify(processos), 200

    except Exception as erro:
        return jsonify({"erro": str(erro)}), 500

    finally:
        if cursor:
            cursor.close()
        conexao.close()


@app.route("/api/processos", methods=["POST"])
def cadastrar_processo():
    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({"erro": "Dados não enviados"}), 400

    nome = dados.get("nome", "").strip()
    tipo = dados.get("tipo", "").strip()
    setor = dados.get("setor", "").strip()

    if not nome or not tipo or not setor:
        return jsonify({"erro": "Preencha todos os campos"}), 400

    conexao = conectar()

    if conexao is None:
        return jsonify({"erro": "Não foi possível conectar ao banco de dados"}), 500

    cursor = None

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO processos (nome, tipo, setor)
            VALUES (%s, %s, %s)
        """, (nome, tipo, setor))

        conexao.commit()

        novo_processo = {
            "id": cursor.lastrowid,
            "nome": nome,
            "tipo": tipo,
            "setor": setor
        }

        return jsonify({
            "mensagem": "Processo cadastrado com sucesso",
            "processo": novo_processo
        }), 201

    except Exception as erro:
        conexao.rollback()
        return jsonify({"erro": str(erro)}), 500

    finally:
        if cursor:
            cursor.close()
        conexao.close()


@app.route("/api/processos/<int:id>", methods=["DELETE"])
def excluir_processo(id):
    conexao = conectar()

    if conexao is None:
        return jsonify({"erro": "Não foi possível conectar ao banco de dados"}), 500

    cursor = None

    try:
        cursor = conexao.cursor()

        cursor.execute(
            "DELETE FROM processos WHERE id = %s",
            (id,)
        )

        conexao.commit()

        if cursor.rowcount == 0:
            return jsonify({"erro": "Processo não encontrado"}), 404

        return jsonify({
            "mensagem": "Processo excluído com sucesso"
        }), 200

    except Exception as erro:
        conexao.rollback()
        return jsonify({"erro": str(erro)}), 500

    finally:
        if cursor:
            cursor.close()
        conexao.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

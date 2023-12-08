from flask import Flask, jsonify
import mysql.connector

read_app = Flask(__name__)

# Configurações do banco de dados
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "financial_hack_db",
}

# Função para obter uma conexão com o banco de dados
def obter_conexao():
    try:
        return mysql.connector.connect(**db_config)
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return None

# Rota para ler todos os dados
@read_app.route("/ler_creditos", methods=["GET"])
def ler_dados():
    try:
        # Conecta ao banco de dados
        conn = obter_conexao()
        if conn is None:
            return jsonify({"erro": "Erro ao conectar ao banco de dados"})

        cursor = conn.cursor(dictionary=True)

        # Executa a consulta SQL para obter todos os dados
        query = "SELECT * FROM emprestimos"
        cursor.execute(query)

        # Obtém todos os dados do resultado da consulta
        dados = cursor.fetchall()

        # Retorna os dados como resposta JSON
        return jsonify(dados)

    except Exception as e:
        return jsonify({"erro": str(e)})

    finally:
        # Fecha a conexão com o banco de dados
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# Rota para ler um dado específico pelo id_emprestimo
@read_app.route("/ler_credito/<int:id_emprestimo>", methods=["GET"])
def ler_dado(id_emprestimo):
    try:
        # Conecta ao banco de dados
        conn = obter_conexao()
        if conn is None:
            return jsonify({"erro": "Erro ao conectar ao banco de dados"})

        cursor = conn.cursor(dictionary=True)

        # Executa a consulta SQL para obter o dado pelo id_emprestimo
        query = "SELECT * FROM emprestimos WHERE id_emprestimo = %s"
        cursor.execute(query, (id_emprestimo,))

        # Obtém o dado do resultado da consulta
        dado = cursor.fetchone()

        if dado:
            return jsonify(dado)
        else:
            return jsonify({"erro": "Registro não encontrado"})

    except Exception as e:
        return jsonify({"erro": str(e)})

    finally:
        # Fecha a conexão com o banco de dados
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    read_app.run(debug=True, port=5003)
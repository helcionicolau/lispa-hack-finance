from flask import Flask, request, jsonify
import mysql.connector
import json
import hashlib

login_app = Flask(__name__)

# Configurações do banco de dados
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "financial_hack_db",
}

def obter_conexao():
    try:
        return mysql.connector.connect(**db_config)
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return None

# Rota para realizar o login
@login_app.route("/login", methods=["POST"])
def login():
    try:
        # Conecta ao banco de dados
        conn = obter_conexao()
        if conn is None:
            return jsonify({"erro": "Erro ao conectar ao banco de dados"})

        cursor = conn.cursor(dictionary=True)

        # Converte a entrada para o formato JSON
        dados_login = json.loads(request.data)

        # Verifica se as chaves essenciais estão presentes nos dados de entrada
        essenciais = ["email", "senha"]
        for chave in essenciais:
            if chave not in dados_login:
                raise ValueError(f"Chave '{chave}' ausente nos dados de entrada")

        email = dados_login["email"]
        senha = dados_login["senha"]

        # Hash da senha
        hashed_senha = hashlib.md5(senha.encode()).hexdigest()

        # Verifica as credenciais no banco de dados
        query = "SELECT * FROM usuarios WHERE email = %s AND senha = %s"
        cursor.execute(query, (email, hashed_senha))

        usuario = cursor.fetchone()

        if usuario:
            return jsonify({"mensagem": "Login bem-sucedido"})
        else:
            return jsonify({"erro": "Credenciais inválidas"})

    except Exception as e:
        return jsonify({"erro": str(e)})

    finally:
        # Fecha a conexão com o banco de dados
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# Rota para criar um novo usuário
@login_app.route("/criar_usuario", methods=["POST"])
def criar_usuario():
    try:
        # Conecta ao banco de dados
        conn = obter_conexao()
        if conn is None:
            return jsonify({"erro": "Erro ao conectar ao banco de dados"})

        cursor = conn.cursor()

        # Converte a entrada para o formato JSON
        dados_usuario = json.loads(request.data)

        # Verifica se as chaves essenciais estão presentes nos dados de entrada
        essenciais = ["nome_usuario", "email", "senha", "telefone"]
        for chave in essenciais:
            if chave not in dados_usuario:
                raise ValueError(f"Chave '{chave}' ausente nos dados de entrada")

        nome_usuario = dados_usuario["nome_usuario"]
        email = dados_usuario["email"]
        senha = dados_usuario["senha"]
        telefone = dados_usuario["telefone"]

        # Hash da senha
        hashed_senha = hashlib.md5(senha.encode()).hexdigest()

        # Insere o novo usuário no banco de dados
        query = "INSERT INTO usuarios (nome_usuario, email, senha, telefone) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (nome_usuario, email, hashed_senha, telefone))

        # Commit da transação
        conn.commit()

        return jsonify({"mensagem": "Usuário criado com sucesso"})

    except Exception as e:
        return jsonify({"erro": str(e)})

    finally:
        # Fecha a conexão com o banco de dados
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    login_app.run(debug=True, port=5001)

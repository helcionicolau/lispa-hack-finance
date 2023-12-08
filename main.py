from flask import Flask, request, jsonify
import mysql.connector
import json
import pickle
import hashlib

app = Flask(__name__)

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
    
# Caminho completo para o modelo treinado
modelo_treinado_path = "./Model/ML_Model.pkl"
with open(modelo_treinado_path, "rb") as model_file:
    try:
        model = pickle.load(model_file)
    except EOFError:
        print("Erro: O arquivo do modelo está vazio ou corrompido.")

# Mapeamento direto para valores categóricos
genero_mapping = {"Female": 0, "Male": 1}
estado_civil_mapping = {"Yes": 1, "No": 0}
dependentes_mapping = {"No": 0, "One": 1, "Two": 2, "More than Two": 3}
edu_mapping = {"Not Graduate": 0, "Graduate": 1}
emp_mapping = {"Job": 0, "Business": 1}
prop_mapping = {"Rural": 0, "Semi-Urban": 1, "Urban": 2}
cred_mapping = {"Between 300 to 500": 0, "Above 500": 1}

# tipo_credito_mapping = {
#     "Salario": 0,
#     "Pessoal": 1,
#     "Automovel": 2,
#     "Particular": 3,
#     "Habitacao": 4,
#     "Seguro": 5,
# }

# ...............................................CRIAR CREDITO..................................................#
# Rota para criar um novo empréstimo
@app.route("/criar_credito", methods=["POST"])
def criar_emprestimo():
    try:
        # Conecta ao banco de dados
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Converte a entrada para o formato JSON
        data_input = json.loads(request.data)

        # Verifica se as chaves essenciais estão presentes nos dados de entrada
        essenciais = [
            "numero_conta",
            "nome_completo",
            "genero",
            "estado_civil",
            "dependentes",
            "educacao",
            "emprego",
            "propriedade",
            "credito",
            "renda_mensal_requerente",
            "renda_mensal_co_requerente",
            "valor_emprestimo",
            "duracao_emprestimo",
            "tipo_credito",
            "email",
        ]
        for chave in essenciais:
            if chave not in data_input:
                raise ValueError(f"Chave '{chave}' ausente nos dados de entrada")

        # Extrai os dados para previsão
        account_no = data_input["numero_conta"]
        fn = data_input["nome_completo"]
        gen = genero_mapping[data_input["genero"]]
        mar = estado_civil_mapping[data_input["estado_civil"]]
        dep = dependentes_mapping[data_input["dependentes"]]
        edu = edu_mapping[data_input["educacao"]]
        emp = emp_mapping[data_input["emprego"]]
        prop = prop_mapping[data_input["propriedade"]]
        cred = cred_mapping[data_input["credito"]]
        mon_income = data_input["renda_mensal_requerente"]
        co_mon_income = data_input["renda_mensal_co_requerente"]
        loan_amt = data_input["valor_emprestimo"]
        dur = data_input["duracao_emprestimo"]
        tipo_credito = data_input["tipo_credito"]
        email = data_input["email"]

        # Converte a duração do empréstimo para meses
        duration = 0
        if dur == 0:
            duration = 60
        elif dur == 1:
            duration = 180
        elif dur == 2:
            duration = 240
        elif dur == 3:
            duration = 360
        elif dur == 4:
            duration = 480

        # Realiza a predição
        features = [
            [
                gen,
                mar,
                dep,
                edu,
                emp,
                float(mon_income),
                float(co_mon_income),
                float(loan_amt),
                duration,
                cred,
                prop,
            ]
        ]
        predicao = model.predict(features)

        # Verifica se o resultado da predição é válido (0 ou 1)
        if predicao[0] not in [0, 1]:
            raise ValueError(f"Resultado inválido da predição: {predicao}")

        # Insere os dados no banco de dados
        insert_data = "INSERT INTO emprestimos (numero_conta, nome_completo, genero, estado_civil, dependentes, educacao, emprego, propriedade, credito, renda_mensal_requerente, renda_mensal_co_requerente, valor_emprestimo, duracao_emprestimo, tipo_credito, email, resultado_predicao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data_values = (
            account_no,
            fn,
            gen,
            mar,
            dep,
            edu,
            emp,
            prop,
            cred,
            float(mon_income),
            float(co_mon_income),
            float(loan_amt),
            float(duration),
            tipo_credito,
            email,
            int(predicao[0]),
        )
        cursor.execute(insert_data, data_values)

        # Commit da transação
        conn.commit()

        # Retorna os resultados como resposta JSON
        return jsonify(
            {
                "numero_conta": account_no,
                "nome_completo": fn,
                "resultado_predicao": int(predicao[0]),
            }
        )

    except Exception as e:
        return jsonify({"erro": str(e)})

    finally:
        # Fecha a conexão com o banco de dados
        if conn.is_connected():
            cursor.close()
            conn.close()


# ...............................................EMPRESTIMO..................................................#
# Rota para atualizar campos específicos de um registro pelo id_emprestimo
@app.route("/atualizar_credito/<int:id_emprestimo>", methods=["PUT"])
def atualizar_registro(id_emprestimo):
    try:
        # Conecta ao banco de dados
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Verifica se o registro existe antes de atualizar
        check_query = "SELECT id_emprestimo FROM emprestimos WHERE id_emprestimo = %s"
        cursor.execute(check_query, (id_emprestimo,))
        resultado = cursor.fetchone()

        if resultado is None:
            return jsonify({"erro": f"Registro com id_emprestimo {id_emprestimo} não encontrado."})

        # Converte a entrada para o formato JSON
        data_input = json.loads(request.data)

        # Atualiza os campos especificados
        update_query = "UPDATE emprestimos SET numero_conta = %s, nome_completo = %s, email = %s, tipo_credito = %s WHERE id_emprestimo = %s"
        data_values = (
            data_input.get("numero_conta", None),
            data_input.get("nome_completo", None),
            data_input.get("email", None),
            data_input.get("tipo_credito", None),
            id_emprestimo,
        )
        cursor.execute(update_query, data_values)

        # Commit da transação
        conn.commit()

        return jsonify({"mensagem": f"Registro com id_emprestimo {id_emprestimo} atualizado com sucesso."})

    except Exception as e:
        return jsonify({"erro": str(e)})

    finally:
        # Fecha a conexão com o banco de dados
        if conn.is_connected():
            cursor.close()
            conn.close()   


# ...............................................USUARIO..................................................#
# Rota para ler todos os dados
@app.route("/ler_usuarios", methods=["GET"])
def ler_dados_usuarios():
    try:
        # Conecta ao banco de dados
        conn = obter_conexao()
        if conn is None:
            return jsonify({"erro": "Erro ao conectar ao banco de dados"})

        cursor = conn.cursor(dictionary=True)

        # Executa a consulta SQL para obter todos os dados
        query = "SELECT * FROM usuarios"
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

# ...............................................LER CREDITOS..................................................#
# Rota para ler todos os dados
@app.route("/ler_creditos", methods=["GET"])
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
@app.route("/ler_credito/<int:id_emprestimo>", methods=["GET"])
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


# ...............................................DEELETAR...............................................#
# Rota para deletar um registro pelo id_emprestimo
@app.route("/deletar_credito/<id_emprestimo>", methods=["GET", "DELETE"])
def deletar_credito(id_emprestimo):
    conn = None  # Defina a variável conn fora do bloco try

    try:
        
        # Conecta ao banco de dados
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Verifica se o registro existe antes de deletar
        check_query = "SELECT id_emprestimo FROM emprestimos WHERE id_emprestimo = %s"
        cursor.execute(check_query, (id_emprestimo,))
        resultado = cursor.fetchone()

        if resultado is None:
            return jsonify({"erro": f"Registro com id_emprestimo {id_emprestimo} não encontrado."})

        # Deleta o registro pelo id_emprestimo
        delete_query = "DELETE FROM emprestimos WHERE id_emprestimo = %s"
        cursor.execute(delete_query, (id_emprestimo,))

        # Commit da transação
        conn.commit()

        return jsonify({"mensagem": f"Registro com id_emprestimo {id_emprestimo} deletado com sucesso."})

    except Exception as e:
        return jsonify({"erro": str(e)})

    finally:
        # Fecha a conexão com o banco de dados
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

                         


# ...............................................LOGIN..................................................#
# Rota para realizar o login
@app.route("/login", methods=["POST"])
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
@app.route("/criar_usuario", methods=["POST"])
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
    app.run(debug=True, host='0.0.0.0')
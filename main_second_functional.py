from flask import Flask, request, jsonify
import mysql.connector
import json
import pickle
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Configurações do banco de dados
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "financial_hack_db",
}

# Caminho completo para o modelo treinado
modelo_treinado_path = "./Model/ML_Model.pkl"
with open(modelo_treinado_path, "rb") as model_file:
    try:
        model = pickle.load(model_file)
    except EOFError:
        print("Erro: O arquivo do modelo está vazio ou corrompido.")

# Rota para prever empréstimo
@app.route("/prever_emprestimo", methods=["POST"])
def prever_emprestimo():
    try:
        # Conecta ao banco de dados
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Converte a entrada para o formato JSON
        data_input = json.loads(request.data)

        # Extrai os dados para previsão
        account_no = data_input["numero_conta"]
        fn = data_input["nome_completo"]
        gen = data_input["genero"]
        mar = data_input["estado_civil"]
        dep = data_input["dependentes"]
        edu = data_input["educacao"]
        emp = data_input["emprego"]
        prop = data_input["propriedade"]
        cred = data_input["credito"]
        mon_income = data_input["renda_mensal_requerente"]
        co_mon_income = data_input["renda_mensal_co_requerente"]
        loan_amt = data_input["valor_emprestimo"]
        dur = data_input["duracao_emprestimo"]

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

        # Mapear valores categóricos para numéricos usando LabelEncoder
        label_encoder = LabelEncoder()
        gen_numeric = label_encoder.fit_transform([gen])[0]
        mar_numeric = label_encoder.fit_transform([mar])[0]
        dep_numeric = label_encoder.fit_transform([dep])[0]
        edu_numeric = label_encoder.fit_transform([edu])[0]
        emp_numeric = label_encoder.fit_transform([emp])[0]
        prop_numeric = label_encoder.fit_transform([prop])[0]
        cred_numeric = label_encoder.fit_transform([cred])[0]

        # Realiza a predição
        features = [
            [
                gen_numeric,
                mar_numeric,
                dep_numeric,
                edu_numeric,
                emp_numeric,
                float(mon_income),
                float(co_mon_income),
                float(loan_amt),
                duration,
                cred_numeric,
                prop_numeric,
            ]
        ]
        predicao = model.predict(features)

        # Verifica se o resultado da predição é válido (0 ou 1)
        if predicao[0] not in [0, 1]:
            raise ValueError(f"Resultado inválido da predição: {predicao}")

        # Insere os dados no banco de dados
        insert_data = "INSERT INTO emprestimos (numero_conta, nome_completo, genero, estado_civil, dependentes, educacao, emprego, propriedade, credito, renda_mensal_requerente, renda_mensal_co_requerente, valor_emprestimo, duracao_emprestimo, resultado_predicao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
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


# Rota para ler todos os dados
@app.route("/ler_dados", methods=["GET"])
def ler_dados():
    try:
        # Conecta ao banco de dados
        conn = mysql.connector.connect(**db_config)
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
        if conn.is_connected():
            cursor.close()
            conn.close()


if __name__ == "__main__":
    app.run(debug=True)
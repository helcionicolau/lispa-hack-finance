# create.py
from flask import Flask, request, jsonify
import mysql.connector
import json
import pickle

create_app = Flask(__name__)

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


# Rota para criar um novo empréstimo
@create_app.route("/criar_credito", methods=["POST"])
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


if __name__ == "__main__":
    create_app.run(debug=True, port=5002)
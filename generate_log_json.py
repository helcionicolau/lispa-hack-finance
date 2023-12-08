import json
import random
from faker import Faker

fake = Faker()

# Mapeamento direto para valores categóricos
genero_mapping = {"Female": 0, "Male": 1}
estado_civil_mapping = {"Yes": 1, "No": 0}
dependentes_mapping = {"No": 0, "One": 1, "Two": 2, "More than Two": 3}
edu_mapping = {"Not Graduate": 0, "Graduate": 1}
emp_mapping = {"Job": 0, "Business": 1}
prop_mapping = {"Rural": 0, "Semi-Urban": 1, "Urban": 2}
cred_mapping = {"Between 300 to 500": 0, "Above 500": 1}

# Função para gerar registros aleatórios
def gerar_registro_aleatorio():
    numero_conta = f"{fake.random_int(min=1, max=999)}"
    registro = {
        "numero_conta": numero_conta,
        "nome_completo": fake.name(),
        "genero": random.choice(list(genero_mapping.keys())),
        "estado_civil": random.choice(list(estado_civil_mapping.keys())),
        "dependentes": random.choice(list(dependentes_mapping.keys())),
        "educacao": random.choice(list(edu_mapping.keys())),
        "emprego": random.choice(list(emp_mapping.keys())),
        "propriedade": random.choice(list(prop_mapping.keys())),
        "credito": random.choice(list(cred_mapping.keys())),
        "renda_mensal_requerente": random.randint(100, 1000),
        "renda_mensal_co_requerente": random.randint(0, 500),
        "valor_emprestimo": random.randint(50000, 200000),
        "duracao_emprestimo": random.randint(1, 5),
    }

    return registro

# Gerar 20 registros aleatórios
registros = [gerar_registro_aleatorio() for _ in range(20)]

# Criar um objeto JSON com a chave "registros"
dados_json = {"emprestimos": registros}

# Salvar registros em um arquivo JSON
with open("registros.json", "w") as json_file:
    json.dump(dados_json, json_file, indent=2)

print("Registros gerados e salvos em 'registros.json'")

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


# Função para gerar registros aleatórios com base em um modelo
def gerar_registro_aleatorio(modelo):
    registro = modelo.copy()

    # Preencher com valores aleatórios
    registro["numero_conta"] = fake.random_int(min=1, max=999)
    registro["nome_completo"] = fake.name()
    registro["genero"] = random.choice(list(genero_mapping.keys()))
    registro["estado_civil"] = random.choice(list(estado_civil_mapping.keys()))
    registro["dependentes"] = random.choice(list(dependentes_mapping.keys()))
    registro["educacao"] = random.choice(list(edu_mapping.keys()))
    registro["emprego"] = random.choice(list(emp_mapping.keys()))
    registro["propriedade"] = random.choice(list(prop_mapping.keys()))
    registro["credito"] = random.choice(list(cred_mapping.keys()))
    registro["renda_mensal_requerente"] = random.randint(100, 1000)
    registro["renda_mensal_co_requerente"] = random.randint(0, 500)
    registro["valor_emprestimo"] = random.randint(50000, 200000)
    registro["duracao_emprestimo"] = random.randint(1, 5)

    return registro


# Dois modelos base
modelo_base_1 = {
    "numero_conta": "013",
    "nome_completo": "Paulo Bunga",
    "genero": "Male",
    "estado_civil": "No",
    "dependentes": "One",
    "educacao": "Graduate",
    "emprego": "Job",
    "propriedade": "Urban",
    "credito": "Above 500",
    "renda_mensal_requerente": 15000,
    "renda_mensal_co_requerente": 200,
    "valor_emprestimo": 500,
    "duracao_emprestimo": 2,
}

modelo_base_2 = {
    "numero_conta": "014",
    "nome_completo": "João Baptista",
    "genero": "Male",
    "estado_civil": "Yes",
    "dependentes": "One",
    "educacao": "Graduate",
    "emprego": "Job",
    "propriedade": "Rural",
    "credito": "Between 300 to 500",
    "renda_mensal_requerente": 150,
    "renda_mensal_co_requerente": 0,
    "valor_emprestimo": 100000,
    "duracao_emprestimo": 2,
}

# Gerar 500 registros aleatórios com base nos dois modelos
registros_modelo_1 = [gerar_registro_aleatorio(modelo_base_1) for _ in range(250)]
registros_modelo_2 = [gerar_registro_aleatorio(modelo_base_2) for _ in range(250)]
registros = registros_modelo_1 + registros_modelo_2

# Salvar registros em um arquivo JSON
with open("registros.json", "w") as json_file:
    json.dump({"emprestimos": registros}, json_file, indent=2)

print("Registros gerados e salvos em 'registros.json'")

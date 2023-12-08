import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib
import csv

# Atualizando o modelo para a versão mais recente do scikit-learn
model = joblib.load('./Model/ML_Model.pkl')

def realizar_previsoes(id_emprestimo, numero_conta, nome_completo, genero, estado_civil, dependentes, educacao,
                       emprego, propriedade, credito, renda_mensal_requerente, renda_mensal_co_requerente,
                       valor_emprestimo, duracao_emprestimo):
    # Mapear os valores para os valores esperados pelo modelo
    features = [[genero, estado_civil, dependentes, educacao, emprego, renda_mensal_requerente,
                 renda_mensal_co_requerente, valor_emprestimo, duracao_emprestimo, credito, propriedade]]

    # Converter strings para valores numéricos usando LabelEncoder
    label_encoder = LabelEncoder()
    for feature_index in [0, 1, 2, 3, 4, 9, 10]:
        features[0][feature_index] = label_encoder.fit_transform([features[0][feature_index]])[0]

    prediction = model.predict(features)

    return {
        'id_emprestimo': id_emprestimo,
        'numero_conta': numero_conta,
        'nome_completo': nome_completo,
        'genero': genero,
        'estado_civil': estado_civil,
        'dependentes': dependentes,
        'educacao': educacao,
        'emprego': emprego,
        'propriedade': propriedade,
        'credito': credito,
        'renda_mensal_requerente': renda_mensal_requerente,
        'renda_mensal_co_requerente': renda_mensal_co_requerente,
        'valor_emprestimo': valor_emprestimo,
        'duracao_emprestimo': duracao_emprestimo,
        'resultado_predicao': int(prediction[0])
    }

def inserir_registro(registro, nome_arquivo='novos_dados.csv'):
    # Salvar os resultados em um arquivo CSV
    with open(nome_arquivo, 'a', newline='', encoding='utf-8') as file:
        csv_writer = csv.DictWriter(file, fieldnames=registro.keys())

        # Verificar se é a primeira linha e escrever cabeçalho se necessário
        if file.tell() == 0:
            csv_writer.writeheader()

        csv_writer.writerow(registro)

# Exemplo de inserção automática
novos_dados_exemplo = {
    'id_emprestimo': 3,
    'numero_conta': '010',
    'nome_completo': 'Fulano de J',
    'genero': 'Male',
    'estado_civil': 'No',
    'dependentes': 'No',
    'educacao': 'Graduate',
    'emprego': 'Job',
    'propriedade': 'Urban',
    'credito': 'Above 500',
    'renda_mensal_requerente': 15000,
    'renda_mensal_co_requerente': 0,
    'valor_emprestimo': 500,
    'duracao_emprestimo': 2,
}

# Realizar previsões nos novos dados de exemplo
resultado = realizar_previsoes(**novos_dados_exemplo)

# Inserir o registro automaticamente
inserir_registro(resultado)

# Exibir os resultados
if resultado['resultado_predicao'] == 0:
    print(
        f"Hello: {resultado['nome_completo']} || "
        f"Account number: {resultado['numero_conta']} || "
        "According to our Calculations, you will not get the loan from Bank"
    )
else:
    print(
        f"Hello: {resultado['nome_completo']} || "
        f"Account number: {resultado['numero_conta']} || "
        'Congratulations!! you will get the loan from Bank'
    )
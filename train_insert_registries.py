import csv
import mysql.connector

# Configurações do banco de dados
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "financial_hack_db",
}

# Nome do arquivo CSV
csv_file = 'Loan_Data/test.csv'

# Conectar ao banco de dados
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Nome da tabela
table_name = 'emprestimos'

# Mapeamento de colunas do arquivo CSV para colunas da tabela MySQL
column_mapping = {
    'Loan_ID': 'id_emprestimo',
    'Gender': 'genero',
    'Married': 'estado_civil',
    'Dependents': 'dependentes',
    'Education': 'educacao',
    'Self_Employed': 'emprego',
    'ApplicantIncome': 'renda_mensal_requerente',
    'CoapplicantIncome': 'renda_mensal_co_requerente',
    'LoanAmount': 'valor_emprestimo',
    'Loan_Amount_Term': 'duracao_emprestimo',
    'Credit_History': 'credito',
    'Property_Area': 'propriedade',
    'Loan_Status': 'resultado_predicao'
}

# Abrir o arquivo CSV e ler os dados
with open(csv_file, 'r', newline='', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)

    # Iterar sobre os registros no CSV
    for row in csv_reader:
        # Mapear os nomes das colunas do CSV para os nomes reais da tabela MySQL
        mapped_row = {column_mapping[key]: value for key, value in row.items()}

        # Gerar instrução SQL de inserção
        insert_query = f"INSERT INTO {table_name} ({', '.join(mapped_row.keys())}) VALUES ({', '.join(['%s']*len(mapped_row))})"

        # Executar a instrução SQL de inserção
        cursor.execute(insert_query, tuple(mapped_row.values()))

# Confirmar as alterações no banco de dados
conn.commit()

# Fechar a conexão
cursor.close()
conn.close()

print("Registros inseridos com sucesso!")

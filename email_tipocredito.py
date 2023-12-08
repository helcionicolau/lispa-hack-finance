import re
from random import choice
from faker import Faker

fake = Faker()

# Função para extrair os valores do INSERT
def extrair_valores_insert(insert_query):
    match = re.search(r"\((.*?)\)", insert_query)
    if match:
        valores = match.group(1).split(', ')
        return valores
    return None

# Função para criar comando UPDATE a partir dos valores extraídos
def gerar_comando_update(valores, email, tipo_credito):
    id_emprestimo = valores[0]  # Substitua pelo índice correto conforme sua estrutura
    comando_update = f"UPDATE `emprestimos` SET `email` = {email}, `tipo_credito` = {tipo_credito} WHERE `id_emprestimo` = {id_emprestimo};"
    return comando_update

# Ler o arquivo de texto com a codificação 'utf-8'
with open('change_date.txt', 'r', encoding='utf-8') as file:
    conteudo = file.read()

# Encontrar todos os comandos INSERT no conteúdo
comandos_insert = re.findall(r"\((.*?)\),", conteudo, re.DOTALL)

# Lista para armazenar os comandos UPDATE gerados
comandos_update = []

# Processar cada comando INSERT
for i, comando_insert in enumerate(comandos_insert):
    valores_insert = extrair_valores_insert(f"({comando_insert})")

    # Gerar nome aleatório sem espaços e sem aspas simples
    nome_completo = fake.name().replace(' ', '').replace("'", "")

    # Gerar email aleatório
    primeiro_nome = nome_completo.split()[0].lower()
    ultimo_nome = nome_completo.split()[-1].lower()
    email = f"'{primeiro_nome}.{ultimo_nome}@gmail.com'"

    # Escolher aleatoriamente um tipo_credito do enum e envolver em aspas simples
    tipos_credito_enum = ['Salario', 'Pessoal', 'Automovel', 'Particular', 'Habitacao', 'Seguro']
    tipo_credito = choice(tipos_credito_enum)
    tipo_credito_formatado = f"'{tipo_credito}'"

    comando_update = gerar_comando_update(valores_insert, email, tipo_credito_formatado)
    comandos_update.append(comando_update)

# Gravar os comandos UPDATE em um arquivo de texto (substituindo o conteúdo existente)        
with open('arquivo_update.txt', 'w', encoding='utf-8') as file:
    for comando_update in comandos_update:
        file.write(comando_update + '\n')

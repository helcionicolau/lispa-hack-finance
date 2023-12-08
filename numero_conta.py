import re
from random import randint

# Função para extrair os valores do INSERT
def extrair_valores_insert(insert_query):
    match = re.search(r"\((.*?)\)", insert_query)
    if match:
        valores = match.group(1).split(', ')
        return valores
    return None

# Função para criar comando UPDATE a partir dos valores extraídos
def gerar_comando_update(valores, numero_conta):
    id_emprestimo = valores[0]  # Substitua pelo índice correto conforme sua estrutura
    comando_update = f"UPDATE `emprestimos` SET `numero_conta` = {numero_conta} WHERE `id_emprestimo` = {id_emprestimo};"
    return comando_update

# Ler o arquivo de texto com a codificação 'utf-8'
with open('change_date.txt', 'r', encoding='utf-8') as file:
    conteudo = file.read()

# Encontrar todos os comandos INSERT no conteúdo
comandos_insert = re.findall(r"\((.*?)\),", conteudo, re.DOTALL)

# Dicionário para rastrear o número_conta por nome_completo
numero_conta_por_nome = {}

# Lista para armazenar os comandos UPDATE gerados
comandos_update = []

# Processar cada comando INSERT
for i, comando_insert in enumerate(comandos_insert):
    valores_insert = extrair_valores_insert(f"({comando_insert})")

    nome_completo = valores_insert[1]  # Substitua pelo índice correto conforme sua estrutura

    # Verificar se o nome_completo já tem um número_conta associado
    if nome_completo in numero_conta_por_nome:
        numero_conta = numero_conta_por_nome[nome_completo]
    else:
        # Gerar número_conta aleatório com pelo menos 3 dígitos e no máximo 6 dígitos
        numero_conta = randint(100, 999999)
        numero_conta_por_nome[nome_completo] = numero_conta

    comando_update = gerar_comando_update(valores_insert, numero_conta)
    comandos_update.append(comando_update)

# Gravar os comandos UPDATE em um arquivo de texto (substituindo o conteúdo existente)        
with open('arquivo_update.txt', 'w', encoding='utf-8') as file:
    for comando_update in comandos_update:
        file.write(comando_update + '\n')

import re
from datetime import datetime, timedelta
from random import randint

# Função para extrair os valores do INSERT
def extrair_valores_insert(insert_query):
    match = re.search(r"\((.*?)\)", insert_query)
    if match:
        valores = match.group(1).split(', ')
        return valores
    return None

# Função para criar comando UPDATE a partir dos valores extraídos
def gerar_comando_update(valores, data_hora):
    id_emprestimo = valores[0]  # Substitua pelo índice correto conforme sua estrutura
    comando_update = f"UPDATE `emprestimos` SET `data_registro` = '{data_hora}' WHERE `id_emprestimo` = {id_emprestimo};"
    return comando_update

# Ler o arquivo de texto com a codificação 'utf-8'
with open('change_date.txt', 'r', encoding='utf-8') as file:
    conteudo = file.read()

# Encontrar todos os comandos INSERT no conteúdo
comandos_insert = re.findall(r"\((.*?)\),", conteudo, re.DOTALL)

# Lista para armazenar os comandos UPDATE gerados
comandos_update = []

# Calcular a quantidade de registros por mês
numero_registros = len(comandos_insert)
registros_por_mes = numero_registros // 12
resto_registros = numero_registros % 12

# Inicializar a data de referência
data_referencia = datetime(2023, 1, 1)

# Inicializar variável para contar quantos registros já foram atualizados
registros_atualizados = 0

# Processar cada comando INSERT
for i, comando_insert in enumerate(comandos_insert):
    valores_insert = extrair_valores_insert(f"({comando_insert})")
    
    # Calcular a data com base na posição atual
    meses_para_adicionar = i // registros_por_mes
    if meses_para_adicionar >= resto_registros:
        meses_para_adicionar = resto_registros
    data_atualizada = data_referencia + timedelta(days=30 * meses_para_adicionar)
    
    # Adicionar uma hora aleatória entre 00:00:00 e 23:59:59
    hora_aleatoria = f"{randint(0, 23):02d}:{randint(0, 59):02d}:{randint(0, 59):02d}"
    data_hora = f"{data_atualizada.strftime('%Y-%m-%d')} {hora_aleatoria}"

    comando_update = gerar_comando_update(valores_insert, data_hora)
    comandos_update.append(comando_update)

    # Incrementar a contagem de registros atualizados
    registros_atualizados += 1

# Se houver registros restantes, distribuir igualmente entre os meses
for i in range(registros_atualizados, numero_registros):
    meses_para_adicionar = i % 12
    data_atualizada = data_referencia + timedelta(days=30 * meses_para_adicionar)
    
    # Adicionar uma hora aleatória entre 00:00:00 e 23:59:59
    hora_aleatoria = f"{randint(0, 23):02d}:{randint(0, 59):02d}:{randint(0, 59):02d}"
    data_hora = f"{data_atualizada.strftime('%Y-%m-%d')} {hora_aleatoria}"

    comando_insert = comandos_insert[i]
    valores_insert = extrair_valores_insert(f"({comando_insert})")
    comando_update = gerar_comando_update(valores_insert, data_hora)
    comandos_update.append(comando_update)

# Gravar os comandos UPDATE em um arquivo de texto (substituindo o conteúdo existente)        
with open('arquivo_update.txt', 'w', encoding='utf-8') as file:
    for comando_update in comandos_update:
        file.write(comando_update + '\n')
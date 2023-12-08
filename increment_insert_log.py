# Lista com os dados do INSERT original
dados_insert_original = [
    (791, '872', 'Miss Monica Allison', '1', '0', '3', '1', '1', '0', '0', 792.00, 412.00, 82657.00, 240, 0),
    (792, '013', 'Paulo Bunga', '1', '1', '1', '1', '0', '0', '0', 150.00, 0.00, 100000.00, 240, 0),
    (793, '010', 'João Baptista', '1', '0', '1', '1', '0', '2', '1', 15000.00, 200.00, 500.00, 240, 1),
    (794, '157', 'Brenda Goodwin', '0', '1', '2', '0', '1', '0', '1', 156.00, 377.00, 130068.00, 240, 0),
    (795, '0111', 'Chad Boseman', '1', '0', '1', '1', '0', '2', '1', 15000.00, 200.00, 500.00, 240, 1),
    (796, '2341', 'Helder Verissmo', '1', '0', '0', '1', '0', '2', '1', 15000.00, 200.00, 500.00, 240, 1),
    (797, '92399', 'Helder Verissmo', '1', '0', '0', '0', '0', '2', '1', 15000.00, 200.00, 500.00, 240, 1),
    (798, '92399', 'Mr.Sebastian', '1', '0', '0', '0', '0', '2', '1', 15000.00, 200.00, 500.00, 240, 1),
    (799, '955', 'Jennifer Parker', '0', '1', '1', '1', '0', '2', '0', 784.00, 337.00, 115037.00, 240, 0),
    (800, '790', 'Joseph Warren', '1', '1', '2', '0', '0', '2', '0', 280.00, 257.00, 138218.00, 360, 0)
]

# Número de vezes que deseja repetir os dados
repeticoes = 40

# Loop para gerar os comandos SQL de INSERT repetidos
comandos_insert_repetidos = []
for i in range(repeticoes):
    for dado in dados_insert_original:
        novo_id_emprestimo = dado[0] + i * len(dados_insert_original)
        novo_dado = (novo_id_emprestimo,) + dado[1:]
        comando_insert = f"INSERT INTO emprestimos VALUES {novo_dado};"
        comandos_insert_repetidos.append(comando_insert)

# Salvar os comandos em um arquivo SQL
with open('comandos_insert_repetidos.sql', 'w') as sql_file:
    for comando in comandos_insert_repetidos:
        sql_file.write(comando + '\n')

print(f"Comandos SQL gerados e salvos em 'comandos_insert_repetidos.sql'")

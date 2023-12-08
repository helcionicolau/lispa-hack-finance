from flask import Flask, request, jsonify
import mysql.connector
import json

update_app = Flask(__name__)

# Configurações do banco de dados
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "financial_hack_db",
}

# Rota para atualizar campos específicos de um registro pelo id_emprestimo
@update_app.route("/atualizar_credito/<int:id_emprestimo>", methods=["PUT"])
def atualizar_registro(id_emprestimo):
    try:
        # Conecta ao banco de dados
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Verifica se o registro existe antes de atualizar
        check_query = "SELECT id_emprestimo FROM emprestimos WHERE id_emprestimo = %s"
        cursor.execute(check_query, (id_emprestimo,))
        resultado = cursor.fetchone()

        if resultado is None:
            return jsonify({"erro": f"Registro com id_emprestimo {id_emprestimo} não encontrado."})

        # Converte a entrada para o formato JSON
        data_input = json.loads(request.data)

        # Atualiza os campos especificados
        update_query = "UPDATE emprestimos SET numero_conta = %s, nome_completo = %s, email = %s, tipo_credito = %s WHERE id_emprestimo = %s"
        data_values = (
            data_input.get("numero_conta", None),
            data_input.get("nome_completo", None),
            data_input.get("email", None),
            data_input.get("tipo_credito", None),
            id_emprestimo,
        )
        cursor.execute(update_query, data_values)

        # Commit da transação
        conn.commit()

        return jsonify({"mensagem": f"Registro com id_emprestimo {id_emprestimo} atualizado com sucesso."})

    except Exception as e:
        return jsonify({"erro": str(e)})

    finally:
        # Fecha a conexão com o banco de dados
        if conn.is_connected():
            cursor.close()
            conn.close()


if __name__ == "__main__":
    update_app.run(debug=True, port=5005)
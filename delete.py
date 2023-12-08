from flask import Flask, request, jsonify
import mysql.connector
import json

delete_app = Flask(__name__)

# Configurações do banco de dados
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "financial_hack_db",
}

# ...............................................DEELETAR...............................................#
# Rota para deletar um registro pelo id_emprestimo
@delete_app.route("/deletar_credito/<int:id_emprestimo>", methods=["DELETE"])
def deletar_registro(id_emprestimo):
    try:
        # Conecta ao banco de dados
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Verifica se o registro existe antes de deletar
        check_query = "SELECT id_emprestimo FROM emprestimos WHERE id_emprestimo = %s"
        cursor.execute(check_query, (id_emprestimo,))
        resultado = cursor.fetchone()

        if resultado is None:
            return jsonify({"erro": f"Registro com id_emprestimo {id_emprestimo} não encontrado."})

        # Deleta o registro pelo id_emprestimo
        delete_query = "DELETE FROM emprestimos WHERE id_emprestimo = %s"
        cursor.execute(delete_query, (id_emprestimo,))

        # Commit da transação
        conn.commit()

        return jsonify({"mensagem": f"Registro com id_emprestimo {id_emprestimo} deletado com sucesso."})

    except Exception as e:
        return jsonify({"erro": str(e)})

    finally:
        # Fecha a conexão com o banco de dados
        if conn.is_connected():
            cursor.close()
            conn.close()


if __name__ == "__main__":
    delete_app.run(debug=True, port=5004)
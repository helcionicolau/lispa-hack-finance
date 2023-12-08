import streamlit as st
import pandas as pd
import mysql.connector

# Função para extrair os tipos de dados dos campos
def extract_data_types():
    # Mapeamento de campos para tipos de dados
    field_mapping = {
        'Account number': 'varchar(255)',
        'Full Name': 'varchar(255)',
        'Gender': 'varchar(255)',
        'Marital Status': 'varchar(255)',
        'Dependents': 'varchar(255)',
        'Education': 'varchar(255)',
        'Employment Status': 'varchar(255)',
        'Property Area': 'varchar(255)',
        'Credit Score': 'varchar(255)',
        "Applicant's Monthly Income($)": 'decimal(10,2)',
        "Co-Applicant's Monthly Income($)": 'decimal(10,2)',
        'Loan Amount': 'decimal(10,2)',
        'Loan Duration': 'int(11)'
    }

    # Exibir os tipos de dados identificados
    st.write("Tipos de dados identificados:")
    st.write(field_mapping)

    # Atualizar tipos de dados na tabela MySQL
    update_data_types(field_mapping)

# Função para atualizar tipos de dados na tabela MySQL
def update_data_types(field_mapping):
    # Configurações do banco de dados
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": "financial_hack_db",
    }

    # Conecta ao banco de dados
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Atualiza tipos de dados na tabela MySQL
        for field, data_type in field_mapping.items():
            update_query = f"ALTER TABLE emprestimos MODIFY COLUMN {field} {data_type};"
            cursor.execute(update_query)

        # Commit da transação
        conn.commit()

        st.write("Tipos de dados na tabela MySQL atualizados com sucesso.")

    except Exception as e:
        # Imprime mensagens de erro
        st.write(f"Erro ao atualizar tipos de dados na tabela MySQL: {str(e)}")

    finally:
        # Fecha a conexão com o banco de dados
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# Chame a função para extrair e atualizar os tipos de dados
extract_data_types()
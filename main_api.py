import pickle
from sklearn.linear_model import LogisticRegression
import pandas as pd

# Carrega o modelo treinado
model = pickle.load(open('./Model/ML_Model.pkl', 'rb'))

def prever_emprestimo(account_no, fn, gen, mar, dep, edu, emp, prop, cred, mon_income, co_mon_income, loan_amt, dur):
    # Mapeia os índices para os nomes originais
    gen_display = ['Feminino', 'Masculino']
    mar_display = ['Não', 'Sim']
    dep_display = ['Não', 'Um', 'Dois', 'Mais de Dois']
    edu_display = ['Não Graduado', 'Graduado']
    emp_display = ['Emprego', 'Negócio']
    prop_display = ['Rural', 'Semi-Urbano', 'Urbano']
    cred_display = ['Entre 300 e 500', 'Acima de 500']

    # Converte os valores numéricos para os nomes originais
    gen = gen_display[int(gen)]
    mar = mar_display[int(mar)]
    dep = dep_display[int(dep)]
    edu = edu_display[int(edu)]
    emp = emp_display[int(emp)]
    prop = prop_display[int(prop)]
    cred = cred_display[int(cred)]

    # Converte a duração do empréstimo para meses
    duration = 0
    if dur == 0:
        duration = 60
    elif dur == 1:
        duration = 180
    elif dur == 2:
        duration = 240
    elif dur == 3:
        duration = 360
    elif dur == 4:
        duration = 480

    # Realiza a predição
    features = [[gen, mar, dep, edu, emp, mon_income, co_mon_income, loan_amt, duration, cred, prop]]
    predicao = model.predict(features)

    return {
        "numero_conta": account_no,
        "nome_completo": fn,
        "genero": gen,
        "estado_civil": mar,
        "dependentes": dep,
        "educacao": edu,
        "emprego": emp,
        "propriedade": prop,
        "credito": cred,
        "renda_mensal": mon_income,
        "renda_mensal_co_aplicante": co_mon_income,
        "valor_emprestimo": loan_amt,
        "duracao_emprestimo": duration,
        "predicao": int(predicao[0])
    }

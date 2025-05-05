import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# ====== Criação das variáveis ======
temperatura = ctrl.Antecedent(np.arange(0, 151, 1), 'temperatura')
corrente = ctrl.Antecedent(np.arange(0, 501, 1), 'corrente')
variacao_tensao = ctrl.Antecedent(np.arange(0, 21, 1), 'variacao_tensao')
risco = ctrl.Consequent(np.arange(0, 101, 1), 'risco')

# ====== Funções de pertinência ======
temperatura['baixa'] = fuzz.trimf(temperatura.universe, [0, 0, 50])
temperatura['media'] = fuzz.trimf(temperatura.universe, [30, 75, 120])
temperatura['alta'] = fuzz.trimf(temperatura.universe, [100, 150, 150])

corrente['baixa'] = fuzz.trimf(corrente.universe, [0, 0, 150])
corrente['media'] = fuzz.trimf(corrente.universe, [100, 250, 400])
corrente['alta'] = fuzz.trimf(corrente.universe, [350, 500, 500])

variacao_tensao['pequena'] = fuzz.trimf(variacao_tensao.universe, [0, 0, 7])
variacao_tensao['media'] = fuzz.trimf(variacao_tensao.universe, [5, 10, 15])
variacao_tensao['grande'] = fuzz.trimf(variacao_tensao.universe, [13, 20, 20])

risco['baixo'] = fuzz.trimf(risco.universe, [0, 0, 30])
risco['moderado'] = fuzz.trimf(risco.universe, [20, 50, 70])
risco['alto'] = fuzz.trimf(risco.universe, [60, 80, 90])
risco['critico'] = fuzz.trimf(risco.universe, [85, 100, 100])

# ====== Regras Fuzzy ======
regras = [
    ctrl.Rule(temperatura['baixa'] & corrente['baixa'] & variacao_tensao['pequena'], risco['baixo']),
    ctrl.Rule(temperatura['media'] & corrente['media'] & variacao_tensao['media'], risco['moderado']),
    ctrl.Rule(temperatura['alta'] | corrente['alta'] | variacao_tensao['grande'], risco['alto']),
    ctrl.Rule(temperatura['alta'] & corrente['alta'] & variacao_tensao['grande'], risco['critico']),
]

# ====== Sistema de Controle ======
sistema_controle = ctrl.ControlSystem(regras)
avaliador_risco = ctrl.ControlSystemSimulation(sistema_controle)

# ====== Simulação ======
def simular_risco(temp, corrente_valor, variacao_valor):
    avaliador_risco.input['temperatura'] = temp
    avaliador_risco.input['corrente'] = corrente_valor
    avaliador_risco.input['variacao_tensao'] = variacao_valor
    avaliador_risco.compute()

    risco_resultado = avaliador_risco.output['risco']
    print(f"\nTemperatura: {temp}°C | Corrente: {corrente_valor}A | Variação de Tensão: {variacao_valor}%")
    print(f"Risco Operacional Estimado: {risco_resultado:.2f}%")

    if risco_resultado > 80:
        print("🚨 ALERTA CRÍTICO! Intervenção imediata necessária.")
    elif risco_resultado > 60:
        print("⚠️ Atenção: Alto risco, monitorar de perto.")
    elif risco_resultado > 30:
        print("🔶 Risco Moderado: Acompanhar comportamento.")
    else:
        print("✅ Risco Baixo: Condições normais.")

# ====== Rodando simulações ======
simular_risco(90, 370, 7)
simular_risco(40, 120, 2)
simular_risco(120, 450, 15)

# ====== Mostrar gráficos ======
temperatura.view()
corrente.view()
variacao_tensao.view()
risco.view()
plt.show()

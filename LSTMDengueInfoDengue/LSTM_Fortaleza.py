import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import keras
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.metrics import RootMeanSquaredError, MeanAbsoluteError
from sklearn.preprocessing import MinMaxScaler
import sklearn
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error

df = pd.read_csv('Fortaleza-Dengue.csv')
df = df.sort_values(by='data_iniSE')

casos_datas = df[['data_iniSE', 'casos']].copy()
print(casos_datas.head())   
#normalização dos dados
scaler = MinMaxScaler(feature_range=(0, 1))
df_normalizado = scaler.fit_transform(casos_datas[['casos']].values)

window_size = 3 #3 semanas 
previsao = []
previsao_real=[]

for i in range(window_size, len(df_normalizado)):
    janela = df_normalizado[i - window_size: i, 0]
    previsao.append(janela)
    previsao_real.append(df_normalizado[i, 0])

previsao = np.array(previsao)
previsao_real = np.array(previsao_real)

#ajustar para o formato esperado [amostras, time steps, features]
previsao = np.reshape(previsao, (previsao.shape[0], previsao.shape[1], 1))
#print(previsao.shape)

#dividir em treino e teste e validação
tam_treino = int(len(previsao) * 0.8)#80% para treinamento
x_treino = previsao[:tam_treino]
y_treino = previsao_real[:tam_treino]

tam_teste = int(len(previsao) * 0.1)#10% para teste
x_teste = previsao[tam_treino:tam_teste + tam_treino]
y_teste = previsao_real[tam_treino:tam_treino + tam_teste]

tam_validacao_inicio = tam_treino + int(len(previsao) * 0.1)
x_validacao = previsao[tam_validacao_inicio:]
y_validacao = previsao_real[tam_validacao_inicio:]

#cria o modelo lstm
model = Sequential()
model.add(LSTM(units=100, return_sequences=True, input_shape=(previsao.shape[1], 1)))
model.add(Dropout(0.3))

model.add(LSTM(units=100, return_sequences=True))
model.add(Dropout(0.3))

model.add(LSTM(units=100))
model.add(Dropout(0.3))
model.add(Dense(units=1))
model.compile(optimizer='adam', loss='mean_squared_error', metrics=[RootMeanSquaredError(), MeanAbsoluteError(), sklearn.metrics.mean_absolute_percentage_error()])


model.fit(x_treino, y_treino, epochs=100, batch_size=12, verbose = 1, validation_data=(x_validacao, y_validacao))
keras.saving.save_model(model, 'LSTM_dengue.keras')


# Previsão no conjunto de treinamento
previsao_treinamento_lstm = model.predict(x_treino)
previsao_treinamento_desnormalizada = scaler.inverse_transform(previsao_treinamento_lstm)
y_treinamento_desnormalizado = scaler.inverse_transform(y_treino.reshape(-1, 1))

# Previsão no conjunto de teste
previsao_teste_lstm = model.predict(x_teste)
previsao_teste_desnormalizada = scaler.inverse_transform(previsao_teste_lstm)
y_teste_desnormalizado = scaler.inverse_transform(y_teste.reshape(-1, 1))

previsao_validacao_lstm = model.predict(x_validacao)
previsao_validacao_desnormalizada = scaler.inverse_transform(previsao_validacao_lstm)
y_validacao_desnormalizado = scaler.inverse_transform(y_validacao.reshape(-1, 1))

previsao_futuro = model.predict(previsao)

"""#calculo das metricas
mae_treinamento = mean_absolute_error(y_treinamento_desnormalizado, previsao_treinamento_desnormalizada)
rmse_treinamento = np.sqrt(mean_squared_error(y_treinamento_desnormalizado, previsao_treinamento_desnormalizada))
mape_treinamento = np.mean(np.abs((y_treinamento_desnormalizado - previsao_treinamento_desnormalizada) / y_treinamento_desnormalizado)) * 100

mae_teste = mean_absolute_error(y_teste_desnormalizado, previsao_teste_desnormalizada)
rmse_teste = np.sqrt(mean_squared_error(y_teste_desnormalizado, previsao_teste_desnormalizada))
mape_teste = np.mean(np.abs((y_teste_desnormalizado - previsao_teste_desnormalizada) / y_teste_desnormalizado)) * 100

mae_validacao = mean_absolute_error(y_validacao_desnormalizado, previsao_validacao_desnormalizada)
rmse_validacao = np.sqrt(mean_squared_error(y_validacao_desnormalizado, previsao_validacao_desnormalizada))
mape_validacao = np.mean(np.abs((y_validacao_desnormalizado - previsao_validacao_desnormalizada) / y_validacao_desnormalizado)) * 100
"""

#tempo de previsao
previsao = 52 #52 semanas = 1 ano
janela_atual = df_normalizado[-window_size:].reshape(1, window_size, 1)
previsoes_futuras = []

for _ in range(previsao):
    proxima_previsao = model.predict(janela_atual, verbose = 0)[0][0]
    #modelo.predict(...) retorna uma matriz de previsão, por isso:
    #[0][0] pega o primeiro valor da previsão.
    #Armazena a previsão na variável proxima_pred.
    previsoes_futuras.append(proxima_previsao)
    #janela_atual[:, 1:, :] → remove o primeiro valor da janela (desliza para a esquerda).
    #[[[proxima_pred]]] → cria uma estrutura com a mesma forma da entrada esperada: (1, 1, 1).
    #np.append(..., axis=1) → adiciona o novo valor previsto ao final da janela, formando uma nova janela com tamanho constante.
    #Essa nova janela_atual será usada na próxima iteração do loop, para gerar a próxima previsão.
    janela_atual = np.append(janela_atual[:, 1:, :], [[[proxima_previsao]]], axis=1)

previsoes_futuras = np.array(previsoes_futuras).reshape(-1, 1)
previsoes_futuras_desnormalizadas = scaler.inverse_transform(previsoes_futuras)

# Geração de datas futuras
ultima_data = pd.to_datetime(casos_datas.iloc[-1, 0])
datas_futuras = [ultima_data + datetime.timedelta(weeks=i+1) for i in range(previsao)]
#datas_futuras = pd.to_datetime(datas_futuras).strftime('%Y-%m-%d')

plt.figure(figsize=(20, 8)) 
#1. todos os dados reais
plt.plot(scaler.inverse_transform(df_normalizado), color='blue', label='Casos Reais')
#2. treinamento
treino_range = range(window_size, window_size + len(previsao_treinamento_desnormalizada))
plt.plot(treino_range, previsao_treinamento_desnormalizada, color='orange', label='Previsão Treinamento')

#3. teste
teste_range = range(tam_treino, tam_treino + len(previsao_teste_desnormalizada))
plt.plot(teste_range, previsao_teste_desnormalizada, color='green', label='Previsão Teste')

#4. validação
validacao_range= range(tam_treino + tam_teste, tam_treino + tam_teste + len(previsao_validacao_desnormalizada))
plt.plot(validacao_range, previsao_validacao_desnormalizada, color='red', label='Previsão Validação')
#5. previsões futuras
inicio_futuro = len(df_normalizado)
futuro_range = range(inicio_futuro, inicio_futuro + len(previsoes_futuras_desnormalizadas))
plt.plot(futuro_range, previsoes_futuras_desnormalizadas, color='purple', label='Previsão Futuro (1 ano)')

#  Linha divisória treino/teste
plt.axvline(x=tam_treino + window_size, color='black', linestyle='--', label='Divisão Treino/Teste')
#linha divisória teste/validação
plt.axvline(x=tam_treino + tam_teste + window_size, color='gray', linestyle='--', label='Divisão Teste/Validação')
plt.title('Previsão de Casos de Dengue em Fortaleza com LSTM')
plt.xlabel('Semanas')
plt.ylabel('Número de Casos')
plt.legend()
plt.grid()
plt.show()
#exibir as previsões futuras
for data, casos in zip(datas_futuras, previsoes_futuras_desnormalizadas):
    print(f'Data: {data}, Previsão de Casos: {int(casos[0])}')

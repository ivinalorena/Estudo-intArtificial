import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt


df_original = pd.read_excel('train_data.xlsx')
df = df_original.iloc[:, :-2]  # Exclui as duas últimas colunas

alvo_df = pd.read_excel('alvo.xlsx')  # DataFrame para manipulação
alvo = alvo_df.values.flatten()  # converter para array 1D

normalizador = MinMaxScaler()
dados_normalizados = normalizador.fit_transform(df.values)


n_linhas_por_paciente = 26
n_pacientes = len(dados_normalizados) // n_linhas_por_paciente

# X com shape (n_pacientes, 26, n_features)
x_final = dados_normalizados[:n_pacientes * n_linhas_por_paciente].reshape(
    (n_pacientes, n_linhas_por_paciente, -1)
)

# y: pegando o rótulo da primeira linha de cada paciente
y_raw = alvo[:n_pacientes * n_linhas_por_paciente].reshape((n_pacientes, n_linhas_por_paciente))
y_final = y_raw[:, 0]
#print(y_raw, y_final)

x_treino, x_teste, y_treino, y_teste = train_test_split(
    x_final, y_final, test_size=0.2, stratify=y_final, random_state=42
)

model = Sequential()
model.add(LSTM(64, input_shape=(n_linhas_por_paciente, x_final.shape[2])))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


history = model.fit(x_treino, y_treino, epochs=20, batch_size=4, validation_data=(x_teste, y_teste))
model.save_weights('pesos_modelo.weights.h5')
model.save("modelo_lstm.h5")

loss, acc = model.evaluate(x_teste, y_teste)
print(f"Acurácia: {acc*100:.2f}%")


y_pred = (model.predict(x_teste) > 0.5).astype(int)

print(confusion_matrix(y_teste, y_pred))
print(classification_report(y_teste, y_pred))

plt.plot(history.history['accuracy'], label='Treino')
plt.plot(history.history['val_accuracy'], label='Validação')
plt.xlabel('Época')
plt.ylabel('Acurácia')
plt.legend()
plt.title('Acurácia por época')
plt.show()
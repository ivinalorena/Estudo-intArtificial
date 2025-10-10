import pandas as pd

df = pd.read_csv('LSTMDengueInfoDengue/Fortaleza-Dengue.csv')
df = df.sort_values(by='data_iniSE')
print(df.head())
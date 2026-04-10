import pandas as pd

df = pd.read_csv('data/solar_data_clean.csv')

print(df.head())
print(df.shape)
print(df.columns)
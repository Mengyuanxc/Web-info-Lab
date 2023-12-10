import pandas as pd

kg_data = pd.read_csv("kg_final.csv", names=['h', 'r', 't'], engine='python')

print(kg_data)
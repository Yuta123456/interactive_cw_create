import pandas as pd

data = pd.read_csv('D:/M1/fashion/optimization/analyze/versatility.csv', header=None)
print(data.corr())
print(data.describe())

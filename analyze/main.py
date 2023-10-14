import pandas as pd

data = pd.read_csv('D:/M1/fashion/optimization/analyze/random_versatility.csv', header=None)
print(data.corr())
print(data.describe())

# print(len(data[data.iloc[:, 1] > data.iloc[:, 3]])) # 0
# print(len(data[data.iloc[:, 1] > data.iloc[:, 5]])) # 259
# print(len(data[data.iloc[:, 2] > data.iloc[:, 4]])) # 500
# print(len(data[data.iloc[:, 3] > data.iloc[:, 5]])) # 500
# print(len(data[data.iloc[:, 0] > data.iloc[:, 4]])) # 499
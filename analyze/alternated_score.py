import pandas as pd

data = pd.read_csv('D:/M1/fashion/optimization/data/alternated_score.csv', header=None)
print(len(data[data.iloc[:,0] <= data.iloc[:, 1]]))
print(len(data[data.iloc[:,1] <= data.iloc[:, 2]]))
print(len(data[data.iloc[:,0] <= data.iloc[:, 2]]))
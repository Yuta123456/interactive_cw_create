import pandas as pd
import math
with open('compatibility.txt', 'r') as f:
    d = f.readlines()
print('read data')
l1 = []
l2 = []

for l in d:
    l = l.strip().split(' ')
    l1.append(float(l[0]))
    l2.append(math.pow(math.e, float(l[1])))
max_l1 = max(l1)
l1 = [l / max_l1 for l in l1]
s1=pd.Series(l1)
s2=pd.Series(l2)

res=s1.corr(s2)

print(res)
print(s2[:10], s1[:10])
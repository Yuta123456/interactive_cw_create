import json
with open('D:/M1/fashion/optimization/data/tops_count.json', 'r', encoding='shift-jis') as f:
    tops_compatibility = json.load(f)

max_count = 0
for _, b in tops_compatibility.items():
    for _, s in b.items():
        for _, v in s.items():
            # print(v)
            max_count = max(max_count, v)

print(max_count)

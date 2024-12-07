from collections import Counter

"""Part one"""

with open("data/1.txt", "r") as infile:
    col1, col2 = zip(*(map(int, line.split()) for line in infile))

print(sum(abs(a - b) for a, b in zip(sorted(col1), sorted(col2))))

"""Part two"""
count = Counter(col2)
print(sum(a * count[a] for a in col1))

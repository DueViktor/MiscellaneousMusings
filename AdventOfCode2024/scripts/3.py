"""Part one

mul(X,Y), where X and Y are each 1-3 digit numbers
"""

import re


def find_match(s) -> int:
    PATTERN = r"mul\((\d{1,3}),(\d{1,3})\)"
    matches = re.findall(PATTERN, s)
    return sum((int(x) * int(y) for x, y in matches))


total = 0


with open("data/3.txt", "r") as infile:
    for line in infile:
        total += find_match(line)

print(total)

"""Part two,

remove everything from the string between 'don't()' and 'do()'"""

total = 0
with open("data/3.txt", "r") as infile:
    txt = infile.read()

    SUB_PATTERN = r"don't\(\).*?(?=do\(\)|$)"
    cleaned = re.sub(SUB_PATTERN, "", txt, flags=re.DOTALL)

    total += find_match(cleaned)

print(total)

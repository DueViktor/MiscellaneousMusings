"""Part one"""


def valid_one(report: list[int]) -> bool:
    l = list()
    for i, _ in enumerate(report):
        try:
            a = report[i] - report[i + 1]
            l.append(a)
        except IndexError:
            pass

    return (all(x > 0 for x in l) or all(x < 0 for x in l)) and all(
        1 <= abs(x) <= 3 for x in l
    )


safe = 0
with open("data/2.txt", "r") as infile:
    for line in infile:
        line = list(map(int, line.split()))

        if valid_one(line):
            safe += 1

print(safe)

"""Part two"""


def valid_two(report: list[int]) -> bool:
    if valid_one(report):
        return True

    permutations = [report[:i] + report[i + 1 :] for i in range(len(report))]
    for permutation in permutations:
        if valid_one(permutation):
            return True

    return False


safe = 0
with open("data/2.txt", "r") as infile:
    for line in infile:
        line = list(map(int, line.split()))

        if valid_two(line):
            safe += 1

print(safe)

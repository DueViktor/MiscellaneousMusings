import numpy as np

# Read the matrix from the file
with open("data/4.txt", "r") as file:
    lines = [[item for item in line.strip()] for line in file]

matrix = np.array(lines)
rows, cols = matrix.shape
TARGET_WORD = "XMAS"
L = len(TARGET_WORD)


def xmas(matrix, ridx, cidx) -> int:
    """Check occurrences of TARGET_WORD in the matrix."""
    count = 0

    # right
    if cidx + L <= cols and "".join(matrix[ridx, cidx : cidx + L]) == TARGET_WORD:
        count += 1

    # left
    if (
        cidx - L >= 0
        and "".join(matrix[ridx, cidx - L + 1 : cidx + 1][::-1]) == TARGET_WORD
    ):
        count += 1

    # Up
    if (
        ridx - L >= 0
        and "".join(matrix[ridx - L + 1 : ridx + 1, cidx][::-1]) == TARGET_WORD
    ):
        count += 1

    # Down

    return count


total = 0
for ridx in range(rows):
    print(ridx)
    for cidx in range(cols):
        total += xmas(matrix, ridx, cidx)

print("Total occurrences of TARGET_WORD:", total)

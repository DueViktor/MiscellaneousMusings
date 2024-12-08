"""Part one"""

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
        cidx - L + 1 >= 0
        and "".join(matrix[ridx, cidx - L + 1 : cidx + 1][::-1]) == TARGET_WORD
    ):
        count += 1

    # up
    if (
        ridx - L + 1 >= 0
        and "".join(matrix[ridx - L + 1 : ridx + 1, cidx][::-1]) == TARGET_WORD
    ):
        count += 1

    # down
    if ridx + L <= rows and "".join(matrix[ridx : ridx + L, cidx]) == TARGET_WORD:
        count += 1

    # diagonal down right
    if (
        ridx + L <= rows
        and cidx + L <= cols
        and "".join(matrix[range(ridx, ridx + L), range(cidx, cidx + L)]) == TARGET_WORD
    ):
        count += 1

    # diagonal down left
    if (
        ridx + L <= rows
        and cidx - L + 1 >= 0
        and "".join(matrix[range(ridx, ridx + L), range(cidx, cidx - L, -1)])
        == TARGET_WORD
    ):
        count += 1

    # diagonal up left
    if (
        ridx - L + 1 >= 0
        and cidx - L + 1 >= 0
        and "".join(matrix[range(ridx, ridx - L, -1), range(cidx, cidx - L, -1)])
        == TARGET_WORD
    ):
        count += 1

    # diagonal up right
    if (
        ridx - L + 1 >= 0
        and cidx + L <= cols
        and "".join(matrix[range(ridx, ridx - L, -1), range(cidx, cidx + L)])
        == TARGET_WORD
    ):
        count += 1

    return count


total = 0
for ridx in range(rows):
    for cidx in range(cols):
        total += xmas(matrix, ridx, cidx)

print(total)

"""Part two
Det er så lol. 
"""


def three_x_three(matrix, ridx, cidx):
    """Extract and return the 3x3 grid starting at (ridx, cidx)."""
    return matrix[ridx : ridx + 3, cidx : cidx + 3]


def mas(subgrid) -> int:
    target = "MAS"
    top_left_bottom_right = "".join(subgrid[0, 0] + subgrid[1, 1] + subgrid[2, 2])
    top_right_bottom_left = "".join(subgrid[0, 2] + subgrid[1, 1] + subgrid[2, 0])

    return (
        top_left_bottom_right == target or top_left_bottom_right[::-1] == target
    ) and (top_right_bottom_left == target or top_right_bottom_left[::-1] == target)


total = 0
for ridx in range(rows - 2):
    for cidx in range(cols - 2):
        subgrid = three_x_three(matrix, ridx, cidx)
        total += mas(subgrid)
print(total)

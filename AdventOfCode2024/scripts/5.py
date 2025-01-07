"""Part one"""

# Read
first_part = True
protocol = list()
updates = list()

with open("data/5.txt", "r") as infile:
    for line in infile.readlines():
        line = line.strip()

        if not line:
            first_part = False
            continue

        if first_part:
            protocol.append(line.split("|"))
        else:
            updates.append(line.split(","))


def validate_update(update):
    valid = True

    for x, y in protocol:

        try:
            xis = [index for index, element in enumerate(update) if element == x]
            yi = update.index(y)  # return the first index
        except ValueError:  # x or y not in list
            continue

        valid = all(xi < yi for xi in xis)

        if not valid:
            break

    return valid


# Process
res = []
invalids = []  # for part two
for update in updates:

    valid = validate_update(update)

    if valid:
        # i guess the length is always odd based on the description
        N = len(update)
        assert N % 2 != 0
        middle_index = N // 2
        res.append(int(update[middle_index]))
    else:
        invalids.append(update)

print(sum(res))

"""Part two -> reorder time """


def keep_swapping_mate(update) -> int:
    
    while not valid(validate_update):
        for x,y in protocol:

        pass

    return 0


mids = 0
for update in invalids:
    mids += keep_swapping_mate(update)

print(mids)

import sys

lines = open(sys.argv[1]).read().splitlines()
lines = [f"#{line}#" for line in lines]
lines = ["#" * len(lines[0])] + lines + ["#" * len(lines[0])]

def search(x: int, y: int, dx: int, dy: int, next) -> int:
    if lines[y][x] != next[-1]:
        return 0

    next.pop()
    if len(next) == 0:
        return 1

    return search(x + dx, y + dy, dx, dy, next)

total = 0
for y in range(len(lines)):
    for x in range(len(lines[y])):
        if lines[y][x] != "A":
            continue
        subtotal = search(x - 1, y - 1, 1, 1, ["S", "A", "M"]) + \
            search(x + 1, y - 1, -1, 1, ["S", "A", "M"]) + \
            search(x - 1, y + 1, 1, -1, ["S", "A", "M"]) + \
            search(x + 1, y + 1, -1, -1, ["S", "A", "M"])
        if subtotal >= 2:
            total += 1

print(total)
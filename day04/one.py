import sys

lines = open(sys.argv[1]).read().splitlines()
lines = [f"#{line}#" for line in lines]
lines = ["#" * len(lines[0])] + lines + ["#" * len(lines[0])]

def search(x: int, y: int, dx: int, dy: int, next) -> int:
    y += dy
    x += dx
    if lines[y][x] != next[-1]:
        return 0

    next.pop()
    if len(next) == 0:
        return 1

    return search(x, y, dx, dy, next)

total = 0
for y in range(len(lines)):
    for x in range(len(lines[y])):
        if lines[y][x] != "X":
            continue
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                total += search(x, y, dx, dy, ["S", "A", "M"])

print(total)
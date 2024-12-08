import sys

input = open(sys.argv[1]).read().splitlines()
map = [f"#{line}#" for line in input]
border = ["#" * len(map[0])]
map = border + map + border

anti = set()

a = []
for y in range(1, len(map) - 1):
    for x in range(1, len(map[y]) - 1):
        if map[y][x] != ".":
            a.append((x, y, map[y][x]))


def add(x, y) -> bool:
    global anti, map
    if x < 1 or y < 1 or y >= len(map) - 1 or x >= len(map[y]) - 1:
        return False
    anti.add((x, y))
    return True


for i in range(len(a)):
    for j in range(i + 1, len(a)):
        if a[i][2] != a[j][2]:
            continue
        dx = a[i][0] - a[j][0]
        dy = a[i][1] - a[j][1]

        x, y = a[i][0], a[i][1]
        while add(x, y):
            x += dx
            y += dy

        x, y = a[j][0], a[j][1]
        while add(x, y):
            x -= dx
            y -= dy

print(len(anti))
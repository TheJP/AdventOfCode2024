import sys

input = open(sys.argv[1]).read().splitlines()
map = [["#"] + [int(e) for e in line] + ["#"] for line in input]
border = [["#"] * len(map[0])]
map = border + map + border

def search(x, y):
    global map
    # visited = set()
    stack = [(x, y)]
    sum = 0
    while len(stack) != 0:
        (x, y) = stack.pop()
        # if (x, y) in visited:
        #     continue
        # visited.add((x, y))
        if map[y][x] == 9:
            sum += 1
            continue
        for (dx, dy) in [1, 0], [0, -1], [-1, 0], [0, 1]:
            if map[y + dy][x + dx] == map[y][x] + 1:
                stack.append((x + dx, y + dy))

    return sum

total = 0
for y in range(1, len(map) - 1):
    for x in range(1, len(map[y]) - 1):
        if map[y][x] == 0:
            total += search(x, y)

print(total)

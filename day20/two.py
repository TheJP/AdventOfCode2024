import sys
from queue import PriorityQueue

input = open(sys.argv[1]).read().splitlines()
map = [list(f"#{line}#") for line in input]
border = [["#"] * len(map[0])]
map = border + map + border

sx, sy = 0, 0
tx, ty = 0, 0
for y, row in enumerate(map):
    for x, cell in enumerate(row):
        if cell == "S":
            sx, sy = x, y
        elif cell == "E":
            tx, ty = x, y
map[sy][sx] = "."
map[ty][tx] = "."

steps = {}

q = PriorityQueue()
visited = set()
q.put((0, (sx, sy)))
while not q.empty():
    d, (rx, ry) = q.get()
    if (rx, ry) in visited:
        continue
    visited.add((rx, ry))
    steps[(rx, ry)] = d

    if rx == tx and ry == ty:
        break

    for dx, dy in [1, 0], [0, -1], [-1, 0], [0, 1]:
        nx, ny = rx + dx, ry + dy
        if (nx, ny) not in visited and map[ny][nx] != "#":
            q.put((d + 1, (nx, ny)))

total = 0
for y in range(2, len(map) - 2):
    for x in range(2, len(map[y]) - 2):
        if map[y][x] == "#":
            continue
        if (x, y) not in steps:
            print("missing")
            raise ValueError()
        for dy in range(-20, 21):
            for dx in range(-20, 21):
                if abs(dy) + abs(dx) > 20 or (x + dx, y + dy) not in steps:
                    continue
                if steps[(x + dx, y + dy)] - steps[(x, y)] - abs(dy) - abs(dx) >= 100:
                    total += 1

print(total)

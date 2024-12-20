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

def steps():
    global map, sx, sy

    q = PriorityQueue()
    visited = set()
    q.put((0, (sx, sy)))
    while not q.empty():
        d, (rx, ry) = q.get()
        if (rx, ry) in visited:
            continue
        visited.add((rx, ry))

        if rx == tx and ry == ty:
            return d

        for dx, dy in [1, 0], [0, -1], [-1, 0], [0, 1]:
            nx, ny = rx + dx, ry + dy
            if (nx, ny) not in visited and map[ny][nx] != "#":
                q.put((d + 1, (nx, ny)))


max_steps = steps()

total = 0
for y in range(2, len(map) - 2):
    for x in range(2, len(map[y]) - 2):
        if map[y][x] == "#":
            map[y][x] = "."
            s = steps()
            # if max_steps - s >= 100:
            if max_steps - s == 12:
                print(x, y)
                total += 1
            map[y][x] = "#"

print(total)
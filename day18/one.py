from queue import Queue
import sys

# S = 7
S = 71
# L = 12
L = 1024

input = open(sys.argv[1]).read().splitlines()
coords = []
for line in input:
    x, y = line.split(",")
    coords.append((int(x), int(y)))

border = ["#"] * (S + 2)
grid = [border]
for y in range(S):
    grid.append(["#"] + (["."] * S) + ["#"])
grid.append(border)

for x, y in coords[:L]:
    grid[y + 1][x + 1] = "#"

x, y = 1, 1
visited = set()
queue = Queue()
queue.put((0, x, y))
visited.add((x, y))

while not queue.empty():
    d, x, y = queue.get()
    if x == S and y == S:
        print(d)
        break

    for dx, dy in [1, 0], [0, -1], [-1, 0], [0, 1]:
        nx, ny = x + dx, y + dy
        if grid[ny][nx] != "#" and (nx, ny) not in visited:
            queue.put((d + 1, nx, ny))
            visited.add((nx, ny))
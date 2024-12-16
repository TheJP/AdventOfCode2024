import math
import sys
from queue import PriorityQueue

input = open(sys.argv[1]).read().splitlines()
map = [list(line.replace("S", ".").replace("E", ".")) for line in input]

rx, ry = 1, len(map) - 2
tx, ty = len(map[0]) - 2, 1
dx, dy = 1, 0

q = PriorityQueue()
visited = set()
q.put((0, (rx, ry), (dx, dy)))
parents = {}
best_d = math.inf

sol = []

while not q.empty():
    d, (rx, ry), (dx, dy) = q.get()
    if d > best_d:
        break
    already_visited = ((rx, ry), (dx, dy)) in visited
    visited.add(((rx, ry), (dx, dy)))

    if rx == tx and ry == ty:
        best_d = d
        sol.append((d, (tx, ty), (dx, dy)))
        continue

    if map[ry + dy][rx + dx] != "#" and ((rx + dx, ry + dy), (dx, dy)) not in visited:
        n = (d + 1, ((rx + dx), (ry + dy)), (dx, dy))
        if not already_visited:
            q.put(n)
        if n not in parents:
            parents[n] = []
        parents[n].append((d, (rx, ry), (dx, dy)))

    cdx, cdy = dy, -dx
    if ((rx, ry), (cdx, cdy)) not in visited:
        n = (d + 1000, (rx, ry), (cdx, cdy))
        if not already_visited:
            q.put(n)
        if n not in parents:
            parents[n] = []
        parents[n].append((d, (rx, ry), (dx, dy)))

    ccdx, ccdy = -dy, dx
    if ((rx, ry), (ccdx, ccdy)) not in visited:
        n = (d + 1000, (rx, ry), (ccdx, ccdy))
        if not already_visited:
            q.put(n)
        if n not in parents:
            parents[n] = []
        parents[n].append((d, (rx, ry), (dx, dy)))


counted = set()
def count(d, xy, dxy):
    global parents, counted

    c = 0 if xy in counted else 1
    counted.add(xy)

    if (d, xy, dxy) in parents:
        ps = sorted(parents[(d, xy, dxy)])
        for (nd, nxy, ndxy) in ps:
            c += count(nd, nxy, ndxy)
        return c
    else:
        return c

total = 0
for d, xy, dxy in sol:
    total += count(d, xy, dxy)


for y, row in enumerate(map):
    for x, cell in enumerate(row):
        if (x, y) in counted:
            print("O", end="")
        else:
            print(cell, end="")
    print()
print()


print(total)

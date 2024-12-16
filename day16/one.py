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
while not q.empty():
    d, (rx, ry), (dx, dy) = q.get()
    if ((rx, ry), (dx, dy)) in visited:
        continue
    visited.add(((rx, ry), (dx, dy)))

    if rx == tx and ry == ty:
        print(d)
        break

    if map[ry + dy][rx + dx] != "#" and ((rx + dx, ry + dy), (dx, dy)) not in visited:
        q.put((d + 1, ((rx + dx), (ry + dy)), (dx, dy)))

    cdx, cdy = dy, -dx
    if ((rx, ry), (cdx, cdy)) not in visited:
        q.put((d + 1000, (rx, ry), (cdx, cdy)))

    ccdx, ccdy = -dy, dx
    if ((rx, ry), (ccdx, ccdy)) not in visited:
        q.put((d + 1000, (rx, ry), (ccdx, ccdy)))


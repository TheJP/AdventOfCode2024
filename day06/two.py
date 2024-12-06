# Still brute-force but ~4x faster.
import sys
from typing import Set, Tuple

input = open(sys.argv[1]).read().splitlines()

obstacles = []
for y in range(len(input)):
    for x in range(len(input[y])):
        if input[y][x] == '^':
            start_gx, start_gy = x + 1, y + 1
        elif input[y][x] == '#':
            obstacles.append((x + 1, y + 1))

input = [f"B{line.replace('^', '.')}B" for line in input]
border = ["B"*len(input[0])]
map = [list(line) for line in border + input + border]


def is_loop() -> Tuple[bool, Set[Tuple[float, float, float, float]]]:
    global map, start_gx, start_gy
    gx, gy = start_gx, start_gy

    visited = set()
    dx, dy = 0, -1
    while map[gy][gx] != 'B':
        if (gx, gy, dx, dy) in visited:
            return (True, visited)
        visited.add((gx, gy, dx, dy))
        if map[gy + dy][gx + dx] != '#':
            gx += dx
            gy += dy
        else:
            dx, dy = -dy, dx
    return (False, visited)


loop, visited = is_loop()
assert(not loop)

loops = 0
checked = set()
for ((x, y, dx, dy)) in visited:
    if (x + dx, y + dy) in checked:
        continue
    if map[y + dy][x + dx] == '.':
        checked.add((x + dx, y + dy))
        map[y + dy][x + dx] = "#"
        loop, _ = is_loop()
        if loop:
            loops += 1
        map[y + dy][x + dx] = "."

print(loops)

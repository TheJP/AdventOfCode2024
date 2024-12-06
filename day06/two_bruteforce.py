import sys

input = open(sys.argv[1]).read().splitlines()

for y in range(len(input)):
    for x in range(len(input[y])):
        if input[y][x] == '^':
            start_gx, start_gy = x + 1, y + 1

input = [f"B{line.replace('^', '.')}B" for line in input]
border = ["B"*len(input[0])]
map = [list(line) for line in border + input + border]

def is_loop() -> bool:
    global map, start_gx, start_gy
    gx, gy = start_gx, start_gy

    visited = set()
    dx, dy = 0, -1
    while map[gy][gx] != 'B':
        if (gx, gy, dx, dy) in visited:
            return True
        visited.add((gx, gy, dx, dy))
        if map[gy + dy][gx + dx] != '#':
            gx += dx
            gy += dy
        else:
            dx, dy = -dy, dx
    return False

loops = 0
for y in range(1, len(map) - 1):
    for x in range(1, len(map[y]) - 1):
        if map[y][x] == ".":
            map[y][x] = "#"
            if is_loop():
                loops += 1
            map[y][x] = "."

print(loops)

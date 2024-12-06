import sys

input = open(sys.argv[1]).read().splitlines()

for y in range(len(input)):
    for x in range(len(input[y])):
        if input[y][x] == '^':
            gx, gy = x + 1, y + 1

input = [f"B{line.replace('^', '.')}B" for line in input]
border = ["B"*len(input[0])]
map = border + input + border

visited = set()
dx, dy = 0, -1
while map[gy][gx] != 'B':
    visited.add((gx, gy))
    if map[gy + dy][gx + dx] != '#':
        gx += dx
        gy += dy
    else:
        dx, dy = -dy, dx


print(len(visited))

import sys

map, moves = open(sys.argv[1]).read().split("\n\n")
map = [list(line) for line in map.splitlines()]

rx, ry = 0, 0
for y in range(1, len(map) - 1):
    for x in range(1, len(map[y]) - 1):
        if map[y][x] == "@":
            rx, ry = x, y
            break
    if rx > 0:
        break

for m in moves:
    match m:
        case ">":
            dx, dy = 1, 0,
        case "v":
            dx, dy = 0, 1,
        case "<":
            dx, dy = -1, 0,
        case "^":
            dx, dy = 0, -1,
        case _:
            # print("invalid", m)
            continue

    x, y = rx + dx, ry + dy
    while True:
        match map[y][x]:
            case "#":
                break
            case ".":
                if abs(y - ry) > 1 or abs(x - rx) > 1:
                    map[y][x] = "O"
                map[ry + dy][rx + dx] = "@"
                map[ry][rx] = "."
                rx += dx
                ry += dy
                break
            case "O":
                pass
        x += dx
        y += dy

total = 0
for y, row in enumerate(map):
    for x, cell in enumerate(row):
        if cell == "O":
            total += 100 * y + x


print(total)

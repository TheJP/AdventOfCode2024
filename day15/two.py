import sys

map, moves = open(sys.argv[1]).read().split("\n\n")
map = [list(line) for line in map.splitlines()]

big_map = []
for y, row in enumerate(map):
    big_row = []
    for x, cell in enumerate(row):
        match cell:
            case ".":
                big_row += [".", "."]
            case "#":
                big_row += ["#", "#"]
            case "O":
                big_row += ["[", "]"]
            case "@":
                big_row += ["@", "."]
    big_map.append(big_row)
map = big_map

def print_map():
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            print(cell, end="")
        print()
    print()

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
    if abs(dx) > 0:
        while True:
            match map[y][x]:
                case "#":
                    break
                case ".":
                    while abs(x - rx) > 1:
                        map[y][min(x, x - dx)] = "["
                        map[y][max(x, x - dx)] = "]"
                        x -= 2 * dx
                    map[ry + dy][rx + dx] = "@"
                    map[ry][rx] = "."
                    rx += dx
                    ry += dy
                    break
                case "[":
                    pass
                case "]":
                    pass
            x += dx
            y += dy
    else:
        xs = [x]
        blocked = False
        crates = []
        while not blocked:
            can_move = True
            new_xs = []
            for x in xs:
                match map[y][x]:
                    case "#":
                        blocked = True
                        can_move = False
                        break
                    case ".":
                        pass
                    case "[":
                        can_move = False
                        new_xs += [x, x + 1]
                        crates.append((x, y))
                    case "]":
                        can_move = False
                        if (x - 1, y) not in crates:
                            new_xs += [x - 1, x]
                            crates.append((x - 1, y))

            if can_move:
                if dy < 0:
                    crates = sorted(crates, key=lambda c: c[1])
                else:
                    crates = sorted(crates, key=lambda c: c[1], reverse=True)
                for (cx, cy) in crates:
                    map[cy + dy][cx] = "["
                    map[cy + dy][cx + 1] = "]"
                    map[cy][cx] = "."
                    map[cy][cx + 1] = "."
                map[ry + dy][rx + dx] = "@"
                map[ry][rx] = "."
                rx += dx
                ry += dy
                break
            else:
                y += dy
            xs = new_xs

total = 0
for y, row in enumerate(map):
    for x, cell in enumerate(row):
        if cell == "[":
            total += 100 * y + x


print(total)

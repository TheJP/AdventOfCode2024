import sys

input = open(sys.argv[1]).read().splitlines()
map = [list(f"#{line}#") for line in input]
border = [["#"] * len(map[0])]
map = border + map + border

total = 0
visited = set()
for y0 in range(1, len(map) - 1):
    for x0 in range(1, len(map[y0]) - 1):
        if (x0, y0) in visited:
            continue
        visited.add((x0, y0))

        t = map[y0][x0]
        stack = [(x0, y0)]
        area = 0
        fence = set()
        while len(stack) > 0:
            (x, y) = stack.pop()
            area += 1
            for (dx, dy) in [1, 0], [0, -1], [-1, 0], [0, 1]:
                (x2, y2) = (x + dx, y + dy)
                if map[y2][x2] == t:
                    if (x2, y2) not in visited:
                        stack.append((x2, y2))
                        visited.add((x2, y2))
                else:
                    fence.add((x2, y2, dx, dy))

        # print(t, area, fence)
        sides = 0
        for (x, y, dx, dy) in fence:
            dx2, dy2 = dy, dx
            if (x + dx2, y + dy2, dx, dy) not in fence:
                sides += 1
        total += area * sides


print(total)

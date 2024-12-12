import sys

input = open(sys.argv[1]).read().splitlines()
map = [list(f"#{line}#") for line in input]
border = [["#"] * len(map[0])]
map = border + map + border

# print(map)

total = 0
visited = set()
for y0 in range(1, len(map) - 1):
    for x0 in range(1, len(map[y0]) - 1):
        # print(map[y0][x0], x0, y0)
        if (x0, y0) in visited:
            continue
        visited.add((x0, y0))

        t = map[y0][x0]
        stack = [(x0, y0)]
        area = 0
        fence = 0
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
                    fence += 1

        # print(t, area, fence)
        total += area * fence


print(total)

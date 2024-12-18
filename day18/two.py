import sys

# S = 7
S = 71

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


def can_reach():
    global grid

    x, y = 1, 1
    visited = set()
    stack = [(0, x, y)]
    visited.add((x, y))

    while len(stack) > 0:
        d, x, y = stack.pop()
        if x == S and y == S:
            return True

        for dx, dy in [1, 0], [0, -1], [-1, 0], [0, 1]:
            nx, ny = x + dx, y + dy
            if grid[ny][nx] != "#" and (nx, ny) not in visited:
                stack.append((d + 1, nx, ny))
                visited.add((nx, ny))

    return False


for bx, by in coords:
    grid[by + 1][bx + 1] = "#"
    if not can_reach():
        print(f"{bx},{by}")
        break

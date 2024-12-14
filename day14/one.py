import sys

W, H = 101, 103
# W, H = 11, 7
T = 100

input = open(sys.argv[1]).read().splitlines()
robots = []
for line in input:
    p, v = line.split()
    px, py = map(int, p.split("=")[1].split(","))
    vx, vy = map(int, v.split("=")[1].split(","))
    robots.append(((px, py), (vx, vy)))

for t in range(T):
    for i in range(len(robots)):
        (px, py), (vx, vy) = robots[i]
        px += vx
        py += vy
        while px < 0:
            px += W
        while py < 0:
            py += H
        while px >= W:
            px -= W
        while py >= H:
            py -= H
        robots[i] = ((px, py), (vx, vy))

tl, tr, bl, br = 0, 0, 0, 0
for (px, py), (vx, vy) in robots:
    if px < W // 2:
        if py < H // 2:
            tl += 1
        elif py > H // 2:
            bl += 1
    elif px > W // 2:
        if py < H // 2:
            tr += 1
        elif py > H // 2:
            br += 1

print(tl * tr * bl * br)
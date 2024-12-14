import sys

W, H = 101, 103
# W, H = 11, 7
T = 10_000

input = open(sys.argv[1]).read().splitlines()
robots = []
for line in input:
    p, v = line.split()
    px, py = map(int, p.split("=")[1].split(","))
    vx, vy = map(int, v.split("=")[1].split(","))
    robots.append(((px, py), (vx, vy)))

for t in range(1, T):
    if t % 100_000 == 0:
        print(t)

    map = [["."] * W for y in range(H)]
    for i in range(len(robots)):
        (px, py), (vx, vy) = robots[i]
        # if t <= 28:
        px += vx
        py += vy
        # else:
        #     px += vx * 103
        #     py += vy * 103
        while px < 0:
            px += W
        while py < 0:
            py += H
        while px >= W:
            px -= W
        while py >= H:
            py -= H
        robots[i] = ((px, py), (vx, vy))
        map[py][px] = "#"

    # tl, tr, bl, br = 0, 0, 0, 0
    # for (px, py), (vx, vy) in robots:
    #     if px < W // 2:
    #         if py < H // 2:
    #             tl += 1
    #         elif py > H // 2:
    #             bl += 1
    #     elif px > W // 2:
    #         if py < H // 2:
    #             tr += 1
    #         elif py > H // 2:
    #             br += 1

    # if bl > 2 * tl and br > 2 * tr and abs(bl - br) < 100 and abs(tl - tr) < 100:
    #     try:

    # Explored the outputs manually and found clustering every 103 steps.
    # Then found a tree at a t which was too high. Used the following loop to
    # find the lowest t which contained the same tree.
    for row in map:
        if "###############################" in "".join(row):
            # if t <= 28:
            print(t)
            # else:
            #     print((t - 28) * 103 + 28)
            for y in range(H):
                for x in range(W):
                    print(map[y][x], end="")
                print()
            print()
            break

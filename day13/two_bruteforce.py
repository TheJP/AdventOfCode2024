import math
import sys

A = 3
B = 1

input = open(sys.argv[1]).read().splitlines()

def is_solved():
    global nb, na, ax, ay, bx, by, sx, sy
    return nb * bx + na * ax == sx and nb * by + na * ay == sy

total = 0
for line in input:
    if line.startswith("Button"):
        x, y = line.split(":")[1].split(",")
        x = int(x.split("+")[1])
        y = int(y.split("+")[1])
        if "A" in line:
            ax, ay = x, y
        else:
            bx, by = x, y
    elif line.startswith("Prize"):
        sx, sy = line.split(":")[1].split(",")
        sx = int(sx.split("=")[1]) + 10000000000000
        sy = int(sy.split("=")[1]) + 10000000000000

        nb = math.ceil(min(sx / bx, sy / by))
        na = 0
        while nb >= 0:
            while nb * bx + na * ax < sx or nb * by + na * ay < sy:
                na += 1

            if is_solved():
                total += na * A + nb * B
                break

            nb -= 1



print(total)

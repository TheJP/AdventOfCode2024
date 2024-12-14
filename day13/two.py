import math
import sys

A = 3
B = 1
OFFSET = 10000000000000

input = open(sys.argv[1]).read().splitlines()

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
        sx = int(sx.split("=")[1]) + OFFSET
        sy = int(sy.split("=")[1]) + OFFSET

        na = (sx * by - sy * bx) / (ax * by - ay * bx)
        nb = (sy - na * ay) / by

        if na - int(na) < 0.00001 and nb - int(nb) < 0.00001:
            total += int(na) * A + int(nb) * B

print(total)

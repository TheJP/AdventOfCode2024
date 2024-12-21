from functools import cache
from itertools import permutations
import math
import sys

door = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [None, "0", "A"],
]

robot = [
    [None, "^", "A"],
    ["<", "v", ">"],
]


# def find(char, pad):
#     for y, row in enumerate(pad):
#         for x, c in enumerate(row):
#             if c == char:
#                 return x, y
#     return None, None

def find(char, pt):
    if pt == "R":
        match char:
            case "^":
                return 1, 0
            case "A":
                return 2, 0
            case "<":
                return 0, 1
            case "v":
                return 1, 1
            case ">":
                return 2, 1
    elif pt == "D":
        match char:
            case "7":
                return 0, 0
            case "8":
                return 1, 0
            case "9":
                return 2, 0
            case "4":
                return 0, 1
            case "5":
                return 1, 1
            case "6":
                return 2, 1
            case "1":
                return 0, 2
            case "2":
                return 1, 2
            case "3":
                return 2, 2
            case "0":
                return 1, 3
            case "A":
                return 2, 3

    raise ValueError((char, pt))


t_cache = {}

@cache
def find_seqs(x, y, c, pt):
    tx, ty = find(c, pt)
    o = []
    if tx > x:
        for _ in range(tx - x):
            o.append((1, 0))
    elif x > tx:
        for _ in range(x - tx):
            o.append((-1, 0))
    if ty > y:
        for _ in range(ty - y):
            o.append((0, 1))
    elif y > ty:
        for _ in range(y - ty):
            o.append((0, -1))

    seq = []
    for p in set(permutations(o)):
        rx, ry = x, y
        no = []
        valid = True
        for dx, dy in p:
            rx += dx
            ry += dy
            if pt == "R" and robot[ry][rx] is None:
                valid = False
                break
            if pt == "D" and door[ry][rx] is None:
                valid = False
                break
            match (dx, dy):
                case (1, 0):
                    no.append(">")
                case (-1, 0):
                    no.append("<")
                case (0, 1):
                    no.append("v")
                case (0, -1):
                    no.append("^")
        if valid:
            no.append("A")
            seq.append("".join(no))

    return seq


def translate(codes, pad, pt):
    global t_cache

    sx, sy = find("A", pt)
    result = []
    for code in codes:
        x, y = sx, sy
        new_codes = [""]
        for c in code:
            tx, ty = find(c, pt)
            next_new_codes = []
            for seq in find_seqs(x, y, c, pt):
                for new_code in new_codes:
                    next_new_codes.append(f"{new_code}{seq}")
            new_codes = next_new_codes

            x, y = tx, ty

        result += new_codes

    min_len = min(map(len, result))
    result = list(filter(lambda r: len(r) == min_len, result))

    return result

@cache
def solve(code: str, depth=25):
    global robot, t_cache

    if depth <= 0:
        return len(code)

    result = 0

    x, y = find("A", "R")
    for c in code:
        tx, ty = find(c, "R")
        min_inner = math.inf
        for seq in find_seqs(x, y, c, "R"):
            current = solve(seq, depth - 1)
            if current < min_inner:
                min_inner = current
        result += min_inner

        x, y = tx, ty

    return result


total = 0

input = open(sys.argv[1]).read().splitlines()
for line in input:
    codes = translate([line], door, "D")
    min_press = min(sum(solve(f"{part}A") for part in code.split("A") if part != "") for code in codes)
    factor = int(line.removesuffix("A"))
    total += min_press * factor

print(total)

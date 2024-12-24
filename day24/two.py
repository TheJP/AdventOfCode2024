# Explorative solution:
# Changed x and y manually and added checks if z_i is correct for any i.
# If z_i was not correct we know there is a problem with some gates near
# of the smallest j for which z_j was incorrect.
#
# The following are my notes. Each numbered line is a gate near an identified
# error. The listed lines contain enough information to know which outputs
# have to be swapped.

# 0: wmn OR gpc -> qnm
# 1: qnm AND rfk -> z35
# 2: qnm XOR rfk -> cfk
# 3: y35 XOR x35 -> rfk
#
# swap(1,2)

# 0: cbj XOR csm -> z11
# 1: tgf OR stp -> csm (good)
# 2: x10 AND y10 -> tgf (good)
# 3: x11 AND y11 -> cbj
# 4: y11 XOR x11 -> qjj
# 5: dnt OR qjj -> mhf
#
# swap(3,4)

# 0: y07 AND x07 -> z07
# 1: x07 XOR y07 -> mvw
# 2: pmc XOR mvw -> gmt
#
# swap(0,2)

# 0: khk OR stg -> z18
# 1: y18 XOR x18 -> hch
# 2: nff AND hch -> stg
# 3: hch XOR nff -> dmn
# 4: x18 AND y18 -> khk
# 5: dmn XOR dsj -> z19
#
# swap(0,3)

import sys

inputs, steps = open(sys.argv[1]).read().split("\n\n")
start_values = { k: int(v) for k, v in map(lambda l: l.split(": "), inputs.splitlines()) }

start_gates = []
for line in steps.splitlines():
    x, op, y, _, z = line.split()
    if line == "qnm AND rfk -> z35":
        z = "cfk"
    if line == "qnm XOR rfk -> cfk":
        z = "z35"
    if line == "x11 AND y11 -> cbj":
        z = "qjj"
    if line == "y11 XOR x11 -> qjj":
        z = "cbj"
    if line == "y07 AND x07 -> z07":
        z = "gmt"
    if line == "pmc XOR mvw -> gmt":
        z = "z07"
    if line == "khk OR stg -> z18":
        z = "dmn"
    if line == "hch XOR nff -> dmn":
        z = "z18"
    start_gates.append((x, op, y, z))

gates = [*start_gates]
values = { k: 0 for k, v in start_values.items() }
for i in range(45):
    values[f"y{i:02}"] = 1
last_defined = set(values.keys())

while len(last_defined) > 0:
    defined = set()
    for i, (x, op, y, z) in enumerate(gates):
        if x in values and y in values and (x in last_defined or y in last_defined):
            match op:
                case "AND":
                    values[z] = values[x] & values[y]
                case "OR":
                    values[z] = values[x] | values[y]
                case "XOR":
                    values[z] = values[x] ^ values[y]
            if z.startswith("z") and values[z] != 1:
                print(z, gates[i])
            defined.add(z)
    last_defined = defined

zs = sorted((k for k in values.keys() if k.startswith("z")), reverse=True)
result = 0
for z in zs:
    result = result << 1
    result |= values[z]

print(result)

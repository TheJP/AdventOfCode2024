import sys

inputs, steps = open(sys.argv[1]).read().split("\n\n")
values = { k: int(v) for k, v in map(lambda l: l.split(": "), inputs.splitlines()) }

gates = []
for line in steps.splitlines():
    x, op, y, _, z = line.split()
    gates.append((x, op, y, z))

last_defined = set(values.keys())

while len(last_defined) > 0:
    defined = set()
    for x, op, y, z in gates:
        if x in values and y in values and (x in last_defined or y in last_defined):
            match op:
                case "AND":
                    values[z] = values[x] & values[y]
                case "OR":
                    values[z] = values[x] | values[y]
                case "XOR":
                    values[z] = values[x] ^ values[y]
            defined.add(z)
    last_defined = defined

zs = sorted((k for k in values.keys() if k.startswith("z")), reverse=True)
result = 0
for z in zs:
    result = result << 1
    result |= values[z]

print(result)
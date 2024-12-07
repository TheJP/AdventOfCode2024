import sys

total = 0

def solve(r, ops):
    if len(ops) == 0:
        yield 0
        return

    rhs = ops[0]
    lhss = solve(r, ops[1:])
    for lhs in lhss:
        if lhs > r:
            continue
        yield lhs + rhs
        yield lhs * rhs
        yield int(str(lhs) + str(rhs))

input = open(sys.argv[1]).read().splitlines()
for line in input:
    result, operands = line.split(":")
    result = int(result)
    operands = list(map(int, operands.split()))

    if result in solve(result, list(reversed(operands))):
        # print("YES", line)
        total += result

print(total)

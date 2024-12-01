import sys

input = open(sys.argv[1]).read().splitlines()
left, right = [], []
for line in input:
    [l, r] = line.split()
    left.append(int(l))
    right.append(int(r))

total = sum(abs(l - r) for l, r in zip(sorted(left), sorted(right)))

print(total)

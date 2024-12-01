import sys

input = open(sys.argv[1]).read().splitlines()
left, right = [], []
for line in input:
    [l, r] = line.split()
    left.append(int(l))
    right.append(int(r))

count = {}
for r in right:
    if r in count:
        count[r] += 1
    else:
        count[r] = 1

total = sum(l * count[l] for l in left if l in count)

print(total)
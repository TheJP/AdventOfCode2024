import sys

disk = []

id = 0
input = open(sys.argv[1]).read().splitlines()
for line in input:
    free = False
    for c in line:
        if not free:
            for i in range(int(c)):
                disk.append(id)
            id += 1
        else:
            for i in range(int(c)):
                disk.append(-1)
        free = not free

r = len(disk) - 1
l = 0
while l < r:
    while l < len(disk) and disk[l] >= 0:
        l += 1
    while r >= 0 and disk[r] < 0:
        r -= 1
    if l >= r:
        break
    disk[l], disk[r] = disk[r], disk[l]

print(sum(pos * id for pos, id in enumerate(disk) if disk[pos] >= 0))

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
while r >= 1:
    while r >= 0 and disk[r] < 0:
        r -= 1
    if r < 1:
        break
    print(r)

    file_size = 0
    id = disk[r]
    for i in range(r, 0, -1):
        if disk[i] != id:
            break
        file_size += 1

    hole = 0
    while hole < r:
        space = 0
        while hole < r and disk[hole] >= 0:
            hole += 1
        for i in range(hole, r):
            if disk[i] >= 0:
                break
            space += 1

        if file_size > space:
            hole += space
            continue
        if hole >= r:
            break

        for i in range(file_size):
            disk[hole + i], disk[r - i] = disk[r - i], disk[hole + i]
        break

    r -= file_size

print(sum(pos * id for pos, id in enumerate(disk) if disk[pos] >= 0))

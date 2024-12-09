# >100x faster with some simple changes.
# There is still a lot of potential to further improve,
# but I'm content with a runtime that is less than 150ms.
import sys

disk = []
gaps = []

def show():
    global disk
    for d in disk:
        if d >= 0:
            print(d, end="")
        else:
            print(".", end="")
    print()

id = 0
input = open(sys.argv[1]).read().splitlines()
for line in input:
    free = False
    for c in line:
        c = int(c)
        if not free:
            for i in range(c):
                disk.append(id)
            id += 1
        else:
            if c > 0:
                gaps.append((len(disk), c))
            for i in range(c):
                disk.append(-1)
        free = not free

best = [None] * 10
for i in range(1, 10):
    for (gi, (_di, size)) in enumerate(gaps):
        if size >= i:
            best[i] = gi
            break
# print(gaps)
# print(best)

done_id = set()
r = len(disk) - 1
while r >= 1:
    while r >= 0 and (disk[r] < 0 or disk[r] in done_id):
        r -= 1
    if r < 1:
        break

    file_size = 0
    id = disk[r]
    for i in range(r, 0, -1):
        if disk[i] != id:
            break
        file_size += 1
    done_id.add(id)

    if best[file_size] is None:
        r -= file_size
        continue

    for gi in range(best[file_size], len(gaps)):
        di, space = gaps[gi]
        if space >= file_size:
            best[file_size] = gi
            break

    gi = best[file_size]
    di, space = gaps[gi]
    if space < file_size:
        best[file_size] = None
        continue

    if di >= r:
        continue

    for i in range(file_size):
        disk[di + i], disk[r - i] = disk[r - i], disk[di + i]
    gaps[gi] = (di + file_size, space - file_size)
    # show()

    r -= file_size


# show()
print(sum(pos * id for pos, id in enumerate(disk) if disk[pos] >= 0))

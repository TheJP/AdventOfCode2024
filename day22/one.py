import sys

def mix(s: int, n: int) -> int:
    return s ^ n

def prune(s: int) -> int:
    return s % 16777216


total = 0

input = open(sys.argv[1]).read().splitlines()
for line in input:
    s = int(line)
    for _ in range(2000):
        s = prune(mix(s, s * 64))
        s = prune(mix(s, s // 32))
        s = prune(mix(s, s * 2048))

    total += s

print(total)

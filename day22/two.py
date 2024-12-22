from functools import cache
from itertools import product
import sys

def mix(s: int, n: int) -> int:
    return s ^ n

def prune(s: int) -> int:
    return s % 16777216


monkeys = []

input = open(sys.argv[1]).read().splitlines()
for line in input:
    s = int(line)
    prices = []
    for _ in range(2000):
        s = prune(mix(s, s << 6))
        s = mix(s, s >> 5)
        s = prune(mix(s, s << 11))
        prices.append(s % 10)
    monkeys.append(prices)

bests = []
for prices in monkeys:
    best = {}
    p1, p2, p3, p4 = prices[:4]
    c1, c2, c3, c4 = 0, p2 - p1, p3 - p2, p4 - p3
    for np in prices[4:]:
        c1, c2, c3, c4 = c2, c3, c4, np - p4
        p1, p2, p3, p4 = p2, p3, p4, np
        if (c1, c2, c3, c4) not in best:
            best[(c1, c2, c3, c4)] = np
    bests.append(best)

total = 0
for changes in product(range(-9, 10), repeat=4):
    sum = 0
    for best in bests:
        if changes in best:
            sum += best[changes]
    total = max(total, sum)

print(total)

from collections import defaultdict
from itertools import combinations
import sys

graph = defaultdict(lambda: [])

input = open(sys.argv[1]).read().splitlines()
for line in input:
    a, b = line.split("-")
    graph[a].append(b)
    graph[b].append(a)

largest = set()

for pc in graph.keys():
    sets = []
    for n in graph[pc]:
        added = False
        for s in sets:
            if all(n in graph[o] for o in s):
                added = True
                s.add(n)
                break
        if not added:
            sets.append(set([n]))
    for s in sets:
        s.add(pc)
        if len(s) > len(largest):
            largest = s


print(",".join(sorted(list(largest))))

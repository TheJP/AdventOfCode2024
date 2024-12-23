from collections import defaultdict
from itertools import combinations
import sys

graph = defaultdict(lambda: [])

input = open(sys.argv[1]).read().splitlines()
for line in input:
    a, b = line.split("-")
    graph[a].append(b)
    graph[b].append(a)

groups = set()

for pc in graph.keys():
    for a, b in combinations(graph[pc], 2):
        if b in graph[a]:
            groups.add((pc, a, b))

total = 0
for g in groups:
    if any(pc.startswith("t") for pc in g):
        total += 1

print(total // 3) # // 3 because we find them in any order

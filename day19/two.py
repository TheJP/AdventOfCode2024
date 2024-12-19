from functools import cache
import sys

types, patterns = open(sys.argv[1]).read().split("\n\n")
types = types.split(", ")
patterns = patterns.splitlines()

@cache
def possible(pattern: str) -> bool:
    global types

    if len(pattern) == 0:
        return 1
    count = 0
    for t in types:
        if not pattern.startswith(t):
            continue
        count += possible(pattern[len(t):])

    return count


total = 0
for pattern in patterns:
    total += possible(pattern)

print(total)

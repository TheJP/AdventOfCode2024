from functools import cache
import sys

types, patterns = open(sys.argv[1]).read().split("\n\n")
types = types.split(", ")
patterns = patterns.splitlines()

@cache
def possible(pattern: str) -> bool:
    global types

    if len(pattern) == 0:
        return True
    for t in types:
        if not pattern.startswith(t):
            continue
        if possible(pattern[len(t):]):
            return True

    return False



total = 0
for pattern in patterns:
    if possible(pattern):
        total += 1

print(total)

from functools import cache
import sys

input = open(sys.argv[1]).read()
numbers = [int(n) for n in input.split()]


@cache
def count(n, blinks):
    if blinks == 0:
        return 1
    if n == 0:
        return count(1, blinks - 1)
    else:
        s = str(n)
        l = len(s)
        if l % 2 == 0:
            mid = l // 2
            return count(int(s[:mid]), blinks - 1) + count(int(s[mid:]), blinks - 1)
        else:
            return count(n * 2024, blinks - 1)


print(sum(count(n, 75) for n in numbers))

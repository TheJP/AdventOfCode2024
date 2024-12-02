import sys

import numpy

input = open(sys.argv[1]).read().splitlines()

safe = 0
for line in input:
    numbers = list(map(int, line.split()))
    is_inc = numbers[1] - numbers[0]
    is_safe = True
    for i in range(len(numbers) - 1):
        diff = numbers[i + 1] - numbers[i]
        if diff == 0 or numpy.sign(is_inc) != numpy.sign(diff) or abs(diff) > 3:
            is_safe = False
            break

    if is_safe:
        safe += 1

print(safe)

import sys
from typing import List

import numpy

def is_safe(numbers: List[int]):
    is_inc = numbers[1] - numbers[0]
    for i in range(len(numbers) - 1):
        diff = numbers[i + 1] - numbers[i]
        if diff == 0 or numpy.sign(is_inc) != numpy.sign(diff) or abs(diff) > 3:
            return False
    return True

input = open(sys.argv[1]).read().splitlines()

safe = 0
for line in input:
    numbers = list(map(int, line.split()))
    if any(is_safe([*numbers[0:i], *numbers[(i+1)::]]) for i in range(len(numbers))):
        safe += 1

print(safe)

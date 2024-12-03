import sys
import re

input = open(sys.argv[1]).read()

total = 0

current = 0
dont = input.find("don't()")
while current >= 0:
    part = input[current:]  if dont < 0 else  input[current:dont]

    matches = re.findall("mul\\(([0-9]+),([0-9]+)\\)", part, re.DOTALL)
    total += sum(int(x) * int(y) for (x, y) in matches)

    current = input.find("do()", dont)
    dont = input.find("don't()", current)

print(total)


# Alternative (similar logic different functions)
total = 0
rest = input
while True:
    parts = rest.split("don't()", maxsplit=1)

    matches = re.findall("mul\\(([0-9]+),([0-9]+)\\)", parts[0], re.DOTALL)
    total += sum(int(x) * int(y) for (x, y) in matches)

    if len(parts) == 1:
        break
    else:
        parts = parts[1].split("do()", maxsplit=1)
        if len(parts) == 1:
            break
        else:
            rest = parts[1]

print(total)

import sys
import re

input = open(sys.argv[1]).read()
matches = re.findall("mul\\(([0-9]+),([0-9]+)\\)", input, re.DOTALL)
print(sum(int(x) * int(y) for (x, y) in matches))

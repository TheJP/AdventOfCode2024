from collections import defaultdict
import sys

rules = defaultdict(lambda: [])

input = open(sys.argv[1]).read().splitlines()
rules_part = True
total = 0
for line in input:
    if line.strip() == "":
        rules_part = False
        continue

    if rules_part:
        x, y = line.split("|")
        rules[x].append(y)
    else:
        order = line.split(",")
        correct = True
        for i in range(len(order)):
            for j in range(i+1, len(order)):
                if order[i] in rules[order[j]]:
                    correct = False

        if not correct:
            ordered = False
            while not ordered:
                ordered = True
                for i in range(len(order)):
                    for j in range(i+1, len(order)):
                        if order[i] in rules[order[j]]:
                            order[i], order[j] = order[j], order[i]
                            ordered = False
            total += int(order[len(order) // 2])

print(total)

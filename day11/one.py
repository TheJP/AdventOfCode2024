import sys

input = open(sys.argv[1]).read()
numbers = [int(n) for n in input.split()]

for i in range(25):
    ns = []
    for n in numbers:
        if n == 0:
            ns.append(1)
        else:
            s = str(n)
            l = len(s)
            if l % 2 == 0:
                mid = l // 2
                ns.append(int(s[:mid]))
                ns.append(int(s[mid:]))
            else:
                ns.append(n * 2024)
    # print(ns)
    numbers = ns

print(len(numbers))

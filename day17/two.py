# 2,4: B = A & 0b111
# 1,5: B = B ^ 5
# 7,5: C = A >> B
# 1,6: B = B ^ 6    --> B = B ^ 3
# 0,3: A = A >> 3
# 4,0: B = B ^ C
# 5,5: OUT B
# 3,0: JNZ 0
ns = list(reversed([2,4,1,5,7,5,1,6,0,3,4,0,5,5,3,0]))

xa = [0]
for i, b in enumerate(ns):
    # Add 3 bits an to a
    #   * an ^ 3 ^ c == b
    #   * ((a << 3) | an) >> (b ^ c ^ 6) == c
    nxa = []
    for a in xa:
        s = []
        for an in range(8):
            na = (a << 3) | an
            for c in range(8):
                if (an ^ 3 ^ c) == b and \
                        ((na >> (b ^ c ^ 6)) & 0b111) == c:
                    nxa.append(na)
                    # print(i, an, c)
                    break
    xa = nxa

print(min(xa))

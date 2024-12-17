import sys

register_starts, program = open(sys.argv[1]).read().split("\n\n")
registers = [int(line.split(":")[1]) for line in register_starts.splitlines()]
program = [int(i) for i in program.split(":")[1].split(",")]

def operand(n):
    global registers
    match n:
        case 0 | 1 | 2 | 3:
            return n
        case 4 | 5 | 6:
            return registers[n - 4]
        case 7:
            print("reserved")
            raise ValueError()

p = 0
outs = []
while p + 1 < len(program):
    i = program[p]
    o = program[p + 1]

    match i:
        case 0:
            registers[0] = int(registers[0] / (2**operand(o)))  # << op(o)
        case 1:
            registers[1] = registers[1] ^ o
        case 2:
            registers[1] = operand(o) % 8  # & 0b111
        case 3:
            if registers[0] != 0:
                p = o
                continue
        case 4:
            registers[1] = registers[1] ^ registers[2]
        case 5:
            outs.append(operand(o) % 8)  # & 0b111
        case 6:
            registers[1] = int(registers[0] / (2**operand(o)))  # << op(o)
        case 7:
            registers[2] = int(registers[0] / (2**operand(o)))  # << op(o)

    # print(i, registers)
    p += 2

print(",".join(map(str, outs)))

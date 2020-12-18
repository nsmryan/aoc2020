import itertools
import sys
from collections import defaultdict

f = open("day18.txt", "r")
#f = open("example.txt", "r")
data = f.read()
lines = [line for line in data.split('\n') if len(line.strip()) > 0]


def eval_line(line):
    cursor = 0
    (cursor, datastack, opstack) = parse(cursor, line)

    print("stacks:")
    print(datastack)
    print(opstack)
    print("")

    result = execute(datastack, opstack)
    print("result = " + str(result))
    print("_________")
    return result

def execute(datastack, opstack):
    datastack.reverse()

    opindex = 0
    while opindex < len(opstack):
        op = opstack[opindex]

        if isinstance(op, list):
            lowerdata = datastack.pop()
            print("exec: " + str(op) + " " + str(lowerdata))
            result = execute(lowerdata, op)
            datastack.append(result)
            print("pushed " + str(result))
        else:
            arg1 = datastack.pop()
            if isinstance(arg1, list):
                lop = opstack[opindex + 1]
                print("lexec: " + str(lop) + " " + str(arg1))
                arg1 = execute(arg1, lop)
                opindex += 1

            arg2 = datastack.pop()
            if isinstance(arg2, list):
                rop = opstack[opindex + 1]
                print("rexec: " + str(rop) + " " + str(arg2))
                arg2 = execute(arg2, rop)
                opindex += 1

            if op == '*':
                print(str(arg1) + " * " + str(arg2))
                datastack.append(arg1 * arg2)
            elif op == '+':
                print(str(arg1) + " + " + str(arg2))
                datastack.append(arg1 + arg2)
        
        opindex += 1

    print("")
    return datastack.pop()

def parse(cursor, line):
    datastack = []
    opstack = []
    acc = 0
    while cursor < len(line):
        if line[cursor].isspace():
            cursor += 1

        elif line[cursor].isdigit():
            start = cursor
            while cursor < len(line) and line[cursor].isdigit():
                cursor += 1
            num = int(line[start:cursor])
            datastack.append(num)

        elif line[cursor] == '*':
            opstack.append('*')
            cursor += 1

        elif line[cursor] == '+':
            opstack.append('+')
            cursor += 1

        elif line[cursor] == "(":
            cursor += 1
            (cursor, lowerdata, lowerop) = parse(cursor, line)
            datastack.append(lowerdata)
            opstack.append(lowerop)

        elif line[cursor] == ")":
            cursor += 1
            break

    return cursor, datastack, opstack


assert(eval_line("2 * 3 + (4 * 5)") == 26)
assert(eval_line("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 437)
assert(eval_line("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 12240)
assert(eval_line("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 13632)

print(sum(map(eval_line, lines)))

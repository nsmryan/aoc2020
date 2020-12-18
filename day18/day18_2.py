import itertools
import sys
from collections import defaultdict

f = open("day18.txt", "r")
#f = open("example.txt", "r")
data = f.read()
lines = [line for line in data.split('\n') if len(line.strip()) > 0]


def eval_line(line):
    cursor = 0
    print(line)

    expr = parse(cursor, line)
    print(expr)

    print("")

    result = execute(expr)
    print("result = " + str(result))
    print("_________")
    return result

def execute(expr):
    datastack = []
    for instr in expr:
        if instr == '+':
            datastack.append(datastack.pop() + datastack.pop())
        elif instr == '*':
            datastack.append(datastack.pop() * datastack.pop())
        else:
            datastack.append(instr)

    return datastack.pop()

def tokenize(line):
    cursor = 0
    tokens = []
    while cursor < len(line):
        if line[cursor].isspace():
            cursor += 1

        elif line[cursor].isdigit():
            start = cursor
            while cursor < len(line) and line[cursor].isdigit():
                cursor += 1
            num = int(line[start:cursor])
            tokens.append(num)

        elif line[cursor] == '+':
            tokens.append('+')
            cursor += 1

        elif line[cursor] == '*':
            tokens.append('*')
            cursor += 1

        elif line[cursor] == "(":
            tokens.append("(")
            cursor += 1

        elif line[cursor] == ")":
            tokens.append(")")
            cursor += 1

    return tokens

def parse(cursor, line):
    tokens = tokenize(line)
    print(tokens)
    expr = []
    postfix(0, tokens, expr)
    return expr

def postfix1(cursor, tokens, expr):
    if tokens[cursor] == '(':
        cursor += 1
        cursor = postfix(cursor, tokens, expr)
    else: # number
        expr.append(tokens[cursor])
        cursor += 1

    return cursor

def postfix(cursor, tokens, expr):
    mults = 0

    while cursor < len(tokens):
        if tokens[cursor] == '+':
            cursor += 1
            cursor = postfix1(cursor, tokens, expr)
            expr.append('+')
        elif tokens[cursor] == '*':
            cursor += 1
            mults += 1
        elif tokens[cursor] == '(':
            cursor += 1
            cursor = postfix(cursor, tokens, expr)
        elif tokens[cursor] == ')':
            cursor += 1
            break
        else: # number
            expr.append(tokens[cursor])
            cursor += 1

    for _ in range(0, mults):
        expr.append('*')

    return cursor


assert(eval_line("2 * 3 + (4 * 5)") == 46)
assert(eval_line("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 1445)
assert(eval_line("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 669060)
assert(eval_line("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 23340)

print(sum(map(eval_line, lines)))

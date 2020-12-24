from collections import deque
import sys

filename = "day24.txt"
#filename = "example.txt"

DIRS = ['e', 'w', 'se', 'sw', 'ne', 'nw']

def parse_line(line):
    index = 0
    dirs = []
    while index < len(line):
        if line[index] in ['w', 'e']:
            dirs.append(line[index])
        else:
            dirs.append(line[index:index+2])
            index += 1

        index += 1

    return dirs

def apply_inv(eq, a, b):
    count = min(eq[a], eq[b])
    eq[a] -= count
    eq[b] -= count

def combine(eq, a, b, c):
    if eq[a] != 0 and eq[b] != 0:
        count = min(eq[a], eq[b])
        eq[a] -= count
        eq[b] -= count
        eq[c] += count

def normalize(dirs):
    eq = {d: 0 for d in DIRS}
    for d in dirs:
        eq[d] = eq[d] + 1

    # apply rules of this commutative group of hex direction
    for _ in range(0, 2):
        apply_inv(eq, 'e', 'w')
        apply_inv(eq, 'se', 'nw')
        apply_inv(eq, 'sw', 'ne')

        combine(eq, 'e', 'sw', 'se')
        combine(eq, 'w', 'se', 'sw')
        combine(eq, 'w', 'ne', 'nw')
        combine(eq, 'e', 'nw', 'ne')
        combine(eq, 'ne', 'se', 'e')
        combine(eq, 'nw', 'sw', 'w')

    return eq

def canonical(eq):
    return (eq['e'], eq['w'], eq['se'], eq['sw'], eq['ne'], eq['nw'])

f = open(filename, "r")
data = f.read()
lines = [line.strip() for line in data.split('\n') if len(line) > 0]


dirs = map(parse_line, lines)
eqs = map(normalize, dirs)
canon = map(canonical, eqs)
counts = {can: 0 for can in canon}
for can in canon:
    counts[can] += 1

count = 0
for can in counts.keys():
    if counts[can] % 2 == 1:
        count += 1

print(count)


from collections import deque
import sys

filename = "day24.txt"
#filename = "example.txt"

DIRS = ['e', 'w', 'se', 'sw', 'ne', 'nw']
mapping = {}
mapping['e'] = [1, 0]
mapping['w'] = [-1, 0]
mapping['ne'] = [0, 1]
mapping['nw'] = [-1, 1]
mapping['se'] = [1, -1]
mapping['sw'] = [0, -1]

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

def combine(a, b):
    return map(sum, zip(a, b))

def adjacent(pos):
    return map(tuple, [combine(pos, offset) for offset in mapping.values()])

def normalize(dirs):
    result = reduce(combine, [mapping[d] for d in dirs])
    return (result[0], result[1])


f = open(filename, "r")
data = f.read()
lines = [line.strip() for line in data.split('\n') if len(line) > 0]


dirs = map(parse_line, lines)
canon = map(normalize, dirs)

counts = {can: 0 for can in canon}
for can in canon:
    counts[can] += 1

floor = set()
for can in counts.keys():
    if counts[can] % 2 == 1:
        floor.add(can)

print(len(floor))

for turn in range(0, 100):
    print(str(turn) + " " + str(len(floor)))
    new_floor = set()
    positions = set(floor)
    for pos in floor:
        for adj in adjacent(pos):
            positions.add(adj)

    for pos in positions:
        count = sum([(adj in floor) for adj in adjacent(pos)])
        if pos in floor:
            if count == 1 or count == 2:
                new_floor.add(pos)
        else:
            if count == 2:
                new_floor.add(pos)

    floor = new_floor

print(len(floor))


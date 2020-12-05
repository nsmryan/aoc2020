f = open("day3.txt", "r")
data = f.read()
lines = data.split('\n')

slopes = filter(lambda line: len(line) > 0 and not line.isspace(), lines)
height = len(slopes)
width = len(slopes[0])

TREE = '#'
EMPTY = '.'

def solve(move):
    pos = (0, 0)

    count = 0
    while pos[1] < height:
        if slopes[pos[1]][pos[0]] == TREE:
            count += 1
        pos = ((pos[0] + move[0]) % width, pos[1] + move[1])

    return count

print(solve((3, 1)))


moves = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
print(reduce(lambda a, b: a * b, map(solve, moves)))

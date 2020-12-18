import itertools
import sys
from collections import defaultdict

f = open("day17.txt", "r")
#f = open("example.txt", "r")
data = f.read()
lines = data.split('\n')


board = defaultdict(lambda: '.')
for y in range(0, len(lines)):
    line = lines[y].strip()
    for x in range(0, len(line)):
        board[(x, y, 0)] = line[x]

def print_board(board):
    maxi = max(board.keys())
    mini = min(board.keys())
    for z in range(mini[2], maxi[2] + 1):
        for y in range(mini[1], maxi[1] + 1):
            for x in range(mini[0], maxi[0] + 1):
                coord = (x, y, z)
                if coord in board:
                    sys.stdout.write(board[coord])
                else:
                    sys.stdout.write('.')
            print("")
        print("")

offsets = [(x, y, z) for x in range(-1, 2) for y in range(-1, 2) for z in range(-1, 2)]
offsets.remove((0,0,0))

def add_coord(coord, offset):
    return tuple(map(sum, zip(coord, offset)))

def step_board(board):
    # TODO need to do this for each coord, not overall!
    maxi = max(board.keys())
    mini = min(board.keys())
    new_board = defaultdict(lambda: '.')
    for z in range(mini[2] - 1, maxi[2] + 2):
        for y in range(mini[1] - 1, maxi[1] + 2):
            for x in range(mini[0] - 1, maxi[0] + 2):
                coord = (x, y, z)
                neighs = [add_coord(coord, offset) for offset in offsets]
                n = sum([1 for neigh in neighs if board[neigh] == '#'])

                #if board[coord] == '#':
                    #print(str(coord) + " " + str(n))
                if board[coord] == '#' and not n in [2,3]:
                    new_board[coord] = '.'
                elif board[coord] == '.' and n == 3:
                    new_board[coord] = '#'
                else:
                    new_board[coord] = board[coord]

    return new_board

def solve(board, iters=6):
    for _ in range(0, iters):
        board = step_board(board)
        #print_board(board)

    return sum([1 for val in board.values() if val == '#'])

active = solve(board)
print(active)



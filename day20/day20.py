import itertools
import sys
import math
import copy
import functools


class Tile():
    def __init__(self, num, pixels, rotation, horiz, vert):
        self.num = num
        self.pixels = [[pixel for pixel in line] for line in pixels]

        self.rotation = rotation
        self.horiz = horiz
        self.vert = vert

        self.id = (num, rotation, horiz, vert)

        self.left = [pixels[y][0] for y in range(0, len(pixels))]
        self.right = [pixels[y][len(pixels[0])-1] for y in range(0, len(pixels))]
        self.top = [pixels[0][x] for x in range(0, len(pixels[0]))]
        self.bottom = [pixels[len(pixels)-1][x] for x in range(0, len(pixels[0]))]

        #print("Tile " + str(num) + ":")
        #print_pixels(pixels)
        #print("")

    def rotate(self, amount):
        pixels = copy.deepcopy(self.pixels)

        for y in range(0, len(pixels)):
            for x in range(0, len(pixels[0])):
                if amount == 1:
                    rot_x = len(pixels) - y - 1
                    rot_y = x
                elif amount == 2:
                    rot_x = len(pixels[0]) - x - 1
                    rot_y = len(pixels) - y - 1
                elif amount == 3:
                    rot_y = len(pixels[0]) - x - 1
                    rot_x = y
                pixels[rot_y][rot_x] = self.pixels[y][x]

        return Tile(self.num, pixels, amount, False, False)

    def flip_vert(self):
        pixels = copy.deepcopy(self.pixels)

        for y in range(0, len(pixels)):
            for x in range(0, len(pixels[0])):
                flip_y = len(pixels) - y - 1
                flip_x = x
                pixels[flip_y][flip_x] = self.pixels[y][x]

        return Tile(self.num, pixels, self.rotation, False, True)

    def flip_horiz(self):
        pixels = copy.deepcopy(self.pixels)

        for y in range(0, len(pixels)):
            for x in range(0, len(pixels[0])):
                flip_x = len(pixels[0]) - x - 1
                flip_y = y
                pixels[flip_y][flip_x] = self.pixels[y][x]

        return Tile(self.num, pixels, self.rotation, True, False)

def print_pixels(pixels):
    print("\n".join(["".join(line) for line in pixels]))

def parse_tile(tile):
    num = int(tile[0][5:-1])
    pixels = tile[1:]
    return Tile(num, pixels, 0, False, False)

def parse_tiles(lines):
    tiles = []
    index = 0
    while index < len(lines):
        start = index
        while len(lines[index]) > 0:
            index += 1
        if start == index:
            break
        end = index

        new_tiles = []
        tile = parse_tile(lines[start:end])
        new_tiles.append(tile)
        new_tiles.append(tile.rotate(1))
        new_tiles.append(tile.rotate(2))
        new_tiles.append(tile.rotate(3))

        for new_tile in new_tiles:
            tiles.append(new_tile)
            tiles.append(new_tile.flip_vert())
            tiles.append(new_tile.flip_horiz())

        index += 1

    return tiles


f = open("day20.txt", "r")
#f = open("example.txt", "r")
data = f.read()
lines = [line.strip() for line in data.split('\n')]

tiles = parse_tiles(lines)

dim = int(math.sqrt(len(set([tile.num for tile in tiles]))))
width = len(tiles[0].pixels[0])
height = len(tiles[0].pixels)

print("dim: " + str(dim))
print("width: " + str(width))
print("height: " + str(height))

lefts = {tile.id: set() for tile in tiles}
rights = {tile.id: set() for tile in tiles}
tops = {tile.id: set() for tile in tiles}
bottoms = {tile.id: set() for tile in tiles}

for tile in tiles:
    for other in tiles:
        if tile.num == other.num:
            continue

        if tile.left == other.right:
            lefts[tile.id].add(other)
        if tile.right == other.left:
            rights[tile.id].add(other)
        if tile.top == other.bottom:
            tops[tile.id].add(other)
        if tile.bottom == other.top:
            bottoms[tile.id].add(other)

ids = list(set([tile.id for tile in tiles]))

tilemap = {(x, y): [tile for tile in tiles] for x in range(0, dim) for y in range(0, dim)}

print("edge constraints")

no_lefts = set([tile for ident in ids for tile in lefts[ident] if len(lefts[ident]) > 0])
no_rights = set([tile for ident in ids for tile in rights[ident] if len(rights[ident]) > 0])
no_tops = set([tile for ident in ids for tile in tops[ident] if len(tops[ident]) > 0])
no_bottoms = set([tile for ident in ids for tile in bottoms[ident] if len(bottoms[ident]) > 0])

for y in range(0, dim):
    for x in range(0, dim):
        valids = set(tilemap[(x, y)])

        if x == 0:
            valids = valids.intersection(no_lefts)

        if y == 0:
            valids = valids.intersection(no_tops)

        if x == dim - 1:
            valids = valids.intersection(no_rights)

        if y == dim - 1:
            valids = valids.intersection(no_bottoms)

        tilemap[(x, y)] = valids

print("propagation")

def check_valid(valids, move_valids, moves, tilemap):
    to_remove = []
    all_moves = [tile.id for valid in valids for tile in moves[valid.id]]
    set_of_valids_moves = set(all_moves)
    for move_valid in move_valids:
        if not move_valid.id in set_of_valids_moves:
            to_remove.append(move_valid)
    return to_remove

def solve(tilemap):
    changed = True
    while changed:
        changed = False

        for y in range(0, dim):
            for x in range(0, dim):
                valids = tilemap[(x, y)]
                if x != 0:
                    left_valids = tilemap[(x-1, y)]
                    to_remove = check_valid(valids, left_valids, lefts, tilemap)
                    changed = changed or (len(to_remove) > 0)
                    [left_valids.remove(rem) for rem in to_remove]

                if x != dim - 1:
                    to_remove = []
                    right_valids = tilemap[(x+1, y)]
                    to_remove = check_valid(valids, right_valids, rights, tilemap)
                    changed = changed or (len(to_remove) > 0)
                    [right_valids.remove(rem) for rem in to_remove]

                if y != 0:
                    to_remove = []
                    top_valids = tilemap[(x, y-1)]
                    to_remove = check_valid(valids, top_valids, tops, tilemap)
                    changed = changed or (len(to_remove) > 0)
                    [top_valids.remove(rem) for rem in to_remove]

                if y != dim - 1:
                    to_remove = []
                    bottom_valids = tilemap[(x, y+1)]
                    to_remove = check_valid(valids, bottom_valids, bottoms, tilemap)
                    changed = changed or (len(to_remove) > 0)
                    [bottom_valids.remove(rem) for rem in to_remove]

solve(tilemap)

corners = set()
for pos in [(0, 0), (0, dim-1), (dim-1, 0), (dim-1, dim-1)]:
    for tile in tilemap[pos]:
        corners.add(tile.num)

print(corners)

print(functools.reduce(lambda a, b: a * b, corners))

tilemap[(0, 0)] = set([list(tilemap[(0, 0)])[0]])
solve(tilemap)

pixels = [['.' for x in range(0, dim * (width - 2))] for y in range(0, dim * (height - 2))]
for y_dim in range(0, dim):
    for x_dim in range(0, dim):
        for sub_y in range(0, height - 2):
            for sub_x in range(0, width - 2):
                x = x_dim * (width - 2) + sub_x
                y = y_dim * (height - 2) + sub_y
                tile = list(tilemap[(x_dim, y_dim)])[0]
                pixels[y][x] = tile.pixels[sub_y + 1][sub_x + 1]

image = Tile(0, pixels, 0, False, False)
base = [image]
base.append(image.rotate(1))
base.append(image.rotate(2))
base.append(image.rotate(3))

images = [image for image in base] + [image.flip_horiz() for image in base] + [image.flip_vert() for image in base]

monster0 = "                  # "
monster1 = "#    ##    ##    ###"
monster2 = " #  #  #  #  #  #   "
monster = [monster0, monster1, monster2]

def count_waves(pixels):
    return sum([1 for line in pixels for pixel in line if pixel == '#'])

def match_monster(monster, pixels, x, y):
    for my in range(0, len(monster)):
        for mx in range(0, len(monster[0])):
            if monster[my][mx] == '#':
                if pixels[y + my][x + mx] != '#':
                    return 0
    return 1

def count_monsters(monster, pixels):
    matches = 0
    for y in range(0, len(pixels)):
        if y + len(monster) >= len(pixels):
            continue
        for x in range(0, len(pixels[0])):
            if x + len(monster[0]) >= len(pixels[0]):
                continue

            matches += match_monster(monster, pixels, x, y)
    return matches

for image in images:
    num_monsters = count_monsters(monster, image.pixels)
    if num_monsters == 0:
        continue

    print("num monsters: " + str(num_monsters))
    num_waves = count_waves(image.pixels)
    print("choppiness: " + str(num_waves - num_monsters * count_waves(monster)))


import itertools
import sys
import math
import copy
import functools


def parse_lines(lines):
    return [parse_line(line) for line in lines if len(line.strip()) > 0]

def parse_line(line):
    parts = line.split("(contains")

    ingreds = [ingred.strip() for ingred in parts[0].split(" ") if len(ingred.strip()) > 0]
    allergens = [allergen.strip() for allergen in parts[1][:-1].split(", ") if len(allergen.strip()) > 0]

    return (ingreds, allergens)

f = open("day21.txt", "r")
#f = open("example.txt", "r")
data = f.read()
lines = [line.strip() for line in data.split('\n')]

foods = parse_lines(lines)

allergens = [allergen for food in foods for allergen in food[1]]
ingreds = [ingred for food in foods for ingred in food[0]]
suspects = {allergen: set(ingreds) for allergen in allergens}

for food in foods:
    for allergen in food[1]:
        print(allergen + ": " + str(food[0]))
        print(suspects[allergen])
        suspects[allergen] = suspects[allergen].intersection(set(food[0]))
        print(suspects[allergen])
        print("")

print(suspects)

suspicious = [food for food_list in suspects.values() for food in food_list]
goods = set([ingred for ingred in ingreds if ingred not in suspicious])

count = 0
for food in foods:
    for ingred in food[0]:
        if ingred in goods:
            count += 1

print("Part 1: " + str(count))

for allergen in suspects.keys():
    #[suspects[allergen].remove(good) for good in goods if good in suspects[allergen]]
    for ingred in suspects[allergen]:
        if ingred in goods:
            print("HHHHMMMMMM")
            exit()

possibles = {food:[] for food in suspicious}
for allergen in suspects.keys():
    for food in suspects[allergen]:
        possibles[food].append(allergen)

for (food, allergens) in possibles.items():
    print(food + ": " + str(allergens))

changed = True
solved = []
while changed:
    changed = False

    items = possibles.items()
    for (food, allergens) in items:
        if len(allergens) == 1:
            if not allergens[0] in solved:
                solved.append(allergens[0])
                changed = True
        else:
            if any([other in possibles[food] for other in solved]):
                [possibles[food].remove(other) for other in solved if other in possibles[food]]
                changed = True
print("solved:")

for (food, allergens) in possibles.items():
    print(food + ": " + str(allergens))

bads = possibles.keys()
bads.sort(key=lambda bad: possibles[bad])

bad_ingred_list = ",".join([food for food in bads])
print("")
print("solution:")
print(bad_ingred_list)


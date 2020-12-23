from collections import deque
import sys


def result(cups):
    cup = 1
    result_list = []
    for index in range(1, len(cups)):
        cup = cups[cup]
        result_list.append(cup)
    return " ".join(map(str, result_list))

def decr(cupvalue):
    if cupvalue == 1:
        nextcup = size
    else:
        nextcup = cupvalue - 1

    return nextcup

def placementindex(currentcup, removed):
    nextcup = decr(currentcup)
    while nextcup in removed:
        nextcup = decr(nextcup)
    return nextcup

def print_cups(cups, current_cup):
    print "(" + str(current_cup) + ")",
    mapcup = current_cup
    for _ in range(1, len(cups)):
        mapcup = cups[mapcup]
        print str(mapcup),
    print("")

part = 2
num_moves = 10000000
size = 1000000

# puzzle input
start = "467528193"
# example input
#start = "389125467"

cup_list = [int(ch) for ch in start]
cups = { cup_list[i] : cup_list[(i + 1) % len(cup_list)] for i in range(0, len(cup_list)) }

#print_cups(cups, cup_list[0])
if part == 2:
    cups[cup_list[-1]] = len(cup_list) + 1
    for index in range(len(cup_list) + 1, size + 1):
        if index != size:
            cups[index] = index + 1
        else:
            cups[index] = cup_list[0]
#print_cups(cups, cup_list[0])

currentcup = cup_list[0]
for move in range(0, num_moves):
    if (move % 100000) == 0:
        print("move: " + str(move))
    #print("-- move " + str(move + 1) + " --")
    #print_cups(cups, currentcup)

    removed = []
    removecup = currentcup
    for _ in range(0, 3):
        removecup = cups[removecup]
        removed.append(removecup)
    removecup = cups[removecup]
    #print("\tremovecup = " + str(removecup))
    #print("\tcurrentcup = " + str(currentcup))
    cups[currentcup] = removecup

    nextcup = placementindex(currentcup, removed)

    #print("\tremoved: " + " ".join(map(str, removed)))
    #print("\tdestination: " + str(nextcup))

    onepastcup = cups[nextcup]
    insertcup = nextcup
    for reinsert in removed:
        cups[insertcup] = reinsert
        insertcup = reinsert
    cups[removed[-1]] = onepastcup

    currentcup = cups[currentcup]
    #print("")

#print_cups(cups, currentcup)

if part == 1:
    print(result(cups))
else:
    print(cups[1] * cups[cups[1]])


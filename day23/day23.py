from collections import deque
import sys


def result(cups):
    startindex = 0
    for index in range(0, len(cups)):
        if cups[index] == '1':
            startindex = index + 1
            break
    result_list = []
    for index in range(0, len(cups) - 1):
        result_list.append(cups[(startindex + index) % len(cups)])
    
    return "".join(result_list)

def decr(cupvalue):
    if cupvalue == '1':
        nextcup = '9'
    else:
        nextcup = str(int(cupvalue) - 1)
    return nextcup

def placementindex(cups, currentcup):
    if str(currentcup) in cups:
        currentindex = cups.index(str(currentcup))
    else:
        currentindex

    currentvalue = cups[currentindex]
    nextcup = decr(currentvalue)
    while not str(nextcup) in cups:
        nextcup = decr(nextcup)

    return nextcup

# puzzle input
#start = "467528193"
# example input
start = "389125467"

cups = [ch for ch in start]

currentcup = start[0]
for move in range(0, 100):
    print("-- move " + str(move + 1) + " --")
    for cup in cups:
        if cup == currentcup:
            print "(" + cup + ")",
        else:
            print cup,
    print("")

    removed = []
    for _ in range(0, 3):
        currentindex = cups.index(currentcup)
        removeindex = (currentindex + 1) % len(cups)
        print('removeindex: ' + str(removeindex) + " " + str(cups))
        removed.append(cups.pop(removeindex))

    nextcup = placementindex(cups, currentcup)

    print("\tremoved: " + " ".join(removed))
    print("\tdestination: " + str(nextcup))

    nextindex = (cups.index(str(nextcup)) + 1)# % len(cups)
    print("\tnextindex: " + str(nextindex))

    for reinsert in reversed(removed):
        cups.insert(int(nextindex), reinsert)

    nextindex = cups.index(currentcup)
    currentcup = cups[(nextindex + 1) % len(cups)]
    print("")

for cup in cups:
    if cup == currentcup:
        print "(" + cup + ")",
    else:
        print cup,
print("")

print(result(cups))


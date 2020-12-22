from collections import deque
import sys


def parse_hands(lines):
    player1 = []
    index = 1
    while len(lines[index]) > 0:
        player1.append(int(lines[index]))
        index += 1

    index += 1
    index += 1
    player2 = []
    while index < len(lines) and len(lines[index]) > 0:
        player2.append(int(lines[index]))
        index += 1

    return player1, player2

def play_round(hand1, hand2):
    card1 = hand1.pop()
    card2 = hand2.pop()
    print(str(card1) + " " + str(card2))
    if card1 > card2:
        hand1.appendleft(card1)
        hand1.appendleft(card2)
    else:
        hand2.appendleft(card2)
        hand2.appendleft(card1)

def play(hand1, hand2):
    while len(hand1) != 0 and len(hand2) != 0:
        play_round(hand1, hand2)

def score(hand):
    return sum([(index + 1) * hand[index] for index in range(0, len(hand))])

def play2(hand1, hand2):
    previous_hands = []
    player1_wins = False
    while (hand1, hand2) not in previous_hands and len(hand1) != 0 and len(hand2) != 0:
        previous_hands.append((deque(hand1), deque(hand2)))
        player1_wins = play_round2(hand1, hand2, previous_hands)

    if (hand1, hand2) in previous_hands:
        #print("recursion rule!")
        player1_wins = True

    return player1_wins

def play_round2(hand1, hand2, previous_hands):
    card1 = hand1.pop()
    card2 = hand2.pop()
    #print(str(card1) + " " + str(card2))

    player1_wins = False
    if len(hand1) >= card1 and len(hand2) >= card2:
        new_deck1 = list(hand1)[-card1:]
        new_deck2 = list(hand2)[-card2:]
        new_hand1 = deque(new_deck1)
        new_hand2 = deque(new_deck2)
        player1_wins = play2(new_hand1, new_hand2)
    else:
        # ties are not possible here
        player1_wins = card1 > card2

    if player1_wins:
        hand1.appendleft(card1)
        hand1.appendleft(card2)
    else:
        hand2.appendleft(card2)
        hand2.appendleft(card1)

    return player1_wins

f = open("day22.txt", "r")
#f = open("example.txt", "r")
data = f.read()
lines = [line.strip() for line in data.split('\n')]

orig_hand1, orig_hand2 = parse_hands(lines)
hand1 = deque(reversed(orig_hand1))
hand2 = deque(reversed(orig_hand2))

play(hand1, hand2)
print("Part 1:")
print(hand1)
print(hand2)

if len(hand1) > 0:
    print(score(hand1))
else:
    print(score(hand2))

print("Part 2:")
hand1 = deque(reversed(orig_hand1))
hand2 = deque(reversed(orig_hand2))

play2(hand1, hand2)
print(hand1)
print(hand2)

if len(hand1) > 0:
    print(score(hand1))
else:
    print(score(hand2))


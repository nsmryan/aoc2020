import itertools
import sys


def parse_rule(rule):
    parts = rule.split(":")
    num = int(parts[0])

    if "a" in parts[1]:
        return (num, 'a')
    elif "b" in parts[1]:
        return (num, 'b')
    else:
        choices = [list(map(int, filter(lambda s: len(s.strip()) > 0, choice.split(" ")))) for choice in parts[1].split("|")]
        return (num, choices)


f = open("day19.txt", "r")
#f = open("example.txt", "r")
data = f.read()
lines = [line.strip() for line in data.split('\n')]



index = 0
while len(lines[index]) > 0:
    index += 1

rules = [parse_rule(rule) for rule in lines[0:index]]
rules = { pair[0]: pair[1] for pair in rules}
messages = [message for message in lines[index + 1:] if len(message.strip()) > 0]


def generate(start):
    rule_stacks = [[start]]
    word_stack = [""]
    words = set()
    while len(rule_stacks) > 0:
        rule_stack = rule_stacks.pop()
        rule_num = rule_stack.pop()
        rule = rules[rule_num]

        if isinstance(rule, str):
            word = word_stack.pop()
            new_word = word + rule
            if len(rule_stack) == 0:
                words.add(new_word)
            else:
                word_stack.append(new_word)
                rule_stacks.append(rule_stack)
        else:
            word = word_stack.pop()
            for choice in rules[rule_num]:
                word_stack.append(word)
                new_rule_stack = [rule for rule in rule_stack]
                rule_stacks.append(new_rule_stack + list(reversed(choice)))

    return words

def match(start_rule, start_word):
    rule_stacks = [[start_rule]]
    word_stack = [start_word]
    words = set()
    while len(rule_stacks) > 0:
        rule_stack = rule_stacks.pop()
        rule_num = rule_stack.pop()
        rule = rules[rule_num]

        if isinstance(rule, str):
            word = word_stack.pop()
            if word[0] == rule:
                new_word = word[1:]
                matched = len(new_word) == 0 and len(rule_stack) == 0
                if matched:
                    return True
                elif len(new_word.strip()) > 0 and len(rule_stack) > 0:
                    word_stack.append(new_word)
                    rule_stacks.append(rule_stack)
        else:
            word = word_stack.pop()
            for choice in rules[rule_num]:
                word_stack.append(word)
                new_rule_stack = [rule for rule in rule_stack]
                rule_stacks.append(new_rule_stack + list(reversed(choice)))

    return False

# only do the part that you want to see the answer for
if len(sys.argv) > 1:
    if int(sys.argv[1]) == 1:
        # generation is much slower then matching here!
        #words = generate(0)
        #answer = sum([1 for message in messages if message in words])

        answer = sum([int(match(0, message)) for message in messages])
        print(answer)
    elif int(sys.argv[1]) == 2:
        rules[8] = [[42], [42, 8]]
        rules[11] = [[42, 31], [42, 11, 31]]
        answer = sum([int(match(0, message)) for message in messages])
        print(answer)


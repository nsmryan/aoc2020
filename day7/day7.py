import itertools

f = open("day7.txt", "r")
data = f.read()
lines = data.split('\n')


class Bag():
    def __init__(self, color, insides):
        self.color = color
        self.insides = insides

bags = {}
links = {}
forward = {}
for line in lines:
    if len(line.strip()) == 0:
        break 

    # remove the period at the end
    line = line.strip()[:-1]

    parts = line.split(" bags contain ")
    outer_color = parts[0]
    bag = Bag(outer_color, [])

    if not outer_color in forward:
        forward[outer_color] = []

    if not outer_color in links:
        links[outer_color] = []

    contents = parts[1].split(",")
    for inside in contents:
        if "no other bags" == inside:
            continue

        inside_paths = inside.strip().split(" ")
        num = int(inside_paths[0])
        color = ' '.join(inside_paths[1:-1])
        bag.insides.append((num, color))

        if not color in links:
            links[color] = []
        links[color].append(outer_color)

        forward[outer_color].append(color)

    bags[outer_color] = bag

seen = set()

current = links['shiny gold']

while len(current) > 0:
    color = current.pop()

    if not color in seen:
        seen.add(color)

        if not color in links:
            continue

        nexts = links[color]
        for next_color in nexts:
            if not next_color in seen:
                current.append(next_color)

print(len(seen))

def solve(current):
    num, color = current
    print(current)

    children = bags[color].insides
    if len(children) == 0:
        return num

    count = num + num * sum(map(solve, children))
    return count

count = solve((1, "shiny gold")) - 1
print(count)


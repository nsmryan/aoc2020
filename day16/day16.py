import itertools

f = open("day16.txt", "r")
#f = open("example.txt", "r")
data = f.read()
lines = data.split('\n')


def parse_range(rang):
    [low, high] = rang.split('-')
    return (int(low), int(high))

def check_within(value):
    def check_range(rang):
        return value >= rang[0] and value <= rang[1]
    return check_range

classes = {}
index = 0
while len(lines[index].strip()) > 0:
    line = lines[index]
    [clas, rang] = line.split(":")
    
    ranges = map(parse_range, rang.split("or"))
    classes[clas] = ranges

    index += 1

# move to "your ticket" line
index += 1

# move to your ticket values
index += 1
my_ticket = list(map(int, lines[index].split(',')))

# move to "nearby tickets"
index += 1

# move to ticket list
index += 1
index += 1

ranges = []
for range_list in classes.values():
    [ranges.append(rang) for rang in range_list]


possible_classes = [classes.keys() for _ in range(0, len(my_ticket))]
error_rate = 0
while index < len(lines):
    line = lines[index]
    if len(line) == 0:
        break

    values = list(map(int, line.split(',')))
    has_error = False
    for value in values:
        checks = list(map(lambda b: not b, map(check_within(value), ranges)))
        if all(checks):
            error_rate += value
            has_error = True

    if not has_error:
        for pos in range(0, len(values)):
            value = values[pos]
            check = check_within(value)

            remaining = []
            for key in possible_classes[pos]:
                valid = any(map(check, classes[key]))
                #print(key + ", " + str(value) + ": " + str(valid) + ", " + str(classes[key]))
                if valid:
                    remaining.append(key)
                else:
                    print("filtered " + str(key) + " from pos " + str(pos))

            possible_classes[pos] = list(set(remaining))

    
    index += 1

changed = True
while changed:
    changed = False

    fixed = [clas[0] for clas in possible_classes if len(clas) == 1]
    print(fixed)

    for pos in range(0, len(possible_classes)):
        clas = possible_classes[pos]
        if len(clas) == 0:
            print("ERROR class was: " + str(clas))
            exit()

        if len(clas) > 1:
            new_clas = [c for c in clas if not c in fixed]
            possible_classes[pos] = new_clas
            changed = True

classes = [clas[0] for clas in possible_classes]

print("error rate: " + str(error_rate))

result = 1
for pos in range(0, len(classes)):
    if classes[pos].startswith("departure"):
        result *= my_ticket[pos]

print("part 2 result: " + str(result))


import itertools

f = open("day6.txt", "r")
data = f.read()
lines = data.split('\n')

groups = []
group = []
for line in lines:
    if line.strip() == "":
        if len(group) > 0:
            groups.append(group)
        group = []
    else:
        group.append(line)

def any_answered(group):
    return len(set(itertools.chain.from_iterable(map(list, group))))

def all_answered(group):
    answers = list(itertools.chain.from_iterable(map(set, map(list, group))))
    answers.sort()
    grouped = itertools.groupby(answers, lambda a: a)
    return len(filter(lambda (key, num): len(list(num)) == len(group), grouped))

def all_answered_dict(group)
    num_inds = len(group)
    answers = {}
    for ind in group:
        for answer in ind:
            if not answer in answers:
                answers[answer] = 0
            answers[answer] += 1

    return len([num_answered for num_answered in answers.values() if num_answered == num_inds])

count = sum(map(any_answered, groups))
print(count)

count = sum(map(all_answered, groups))
print(count)

f = open("day1.txt", "r")
data = f.read()
lines = data.split('\n')

used_lines = filter(lambda line: len(line) > 0 and not line.isspace(), lines)
expenses = map(int, used_lines)

for i in range(0, len(expenses)):
    for j in range(i+1, len(expenses)):
        for k in range(j+1, len(expenses)):
            if expenses[i] + expenses[j] + expenses[k] == 2020:
                print(expenses[i] * expenses[j] * expenses[k])
                exit()


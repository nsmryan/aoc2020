def decode(line):
    parts = line.split(":")
    password = parts[1]
    (rang, ch) = parts[0].split(" ")
    (low, high) = rang.split("-")
    return (int(low), int(high), ch, password.strip())

def count_occurances(password):
    counts = {}
    for ch in password:
        if not ch in counts.keys():
            counts[ch] = 0
        counts[ch] += 1

    return counts

def valid(entry):
    (low, high, ch, password) = entry

    first = password[low-1] == ch
    second = password[high-1] == ch
    
    return (first or second) and (not first or not second)


f = open("day2.txt", "r")
data = f.read()
lines = data.split('\n')

used_lines = filter(lambda line: len(line) > 0 and not line.isspace(), lines)
entries = map(decode, used_lines)

counts = sum(map(valid, entries))

print(counts)


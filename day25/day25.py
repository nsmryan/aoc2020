key1 = 8184785
key2 = 5293040
#key1 = 17807724
#key2 = 5764801

def step(value, subject):
    return (value * subject) % 20201227

def find_loop(key):
    value = 1
    loop_times = 0
    while value != key:
        value = step(value, 7)
        loop_times += 1
    return loop_times

loop1 = find_loop(key1)
print("loop size " + str(loop1))
loop2 = find_loop(key2)
print("loop size " + str(loop2))

result = 1
for _ in range(0, loop1):
    result = step(result, key2)
print(result)

result = 1
for _ in range(0, loop2):
    result = step(result, key1)
print(result)

    


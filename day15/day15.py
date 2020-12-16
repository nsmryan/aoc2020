
def solve(inputs, iters=2020, debug=False):
    print("")
    board = { inputs[pos]: pos + 1 for pos in range(0, len(inputs)) }

    spoke = 0
    board[inputs[-1]] = len(inputs) + 1

    spoken = [n for n in inputs]
    spoken.append(spoke)
    for turn in range(len(inputs) + 2, iters + 1):
        if debug: print("turn: " + str(turn))
        if spoke in board:
            diff = turn - board[spoke] - 1
            board[spoke] = turn - 1
            last_last = spoke
            spoke = diff
            if debug: print("\t" + str(last_last) + " = " + str(turn - 1) + " spoke = " + str(spoke))
        else:
            board[spoke] = turn - 1
            if debug: print("\t" + str(spoke) + " = " + str(turn - 1) + " spoke = 0")
            spoke = 0
        
        if debug: print("\t" + str(spoke) + " " + str(board))
        spoken.append(spoke)

    if debug: print(spoken)
    print(spoken[-20:])
    print(len(spoken))
    return spoke


print(str(solve([0,3,6], 16, debug=True)))
print(str(solve([0,3,6], iters=2025)) + " == " + str(436))
exit()
print(str(solve([1,3,2], 2025)) + " == " + str(1))
print(str(solve([2,1,3], 2025)) + " == " + str(10))
print(str(solve([1,2,3], 2025)) + " == " + str(27))
print(str(solve([2,3,1], 2025)) + " == " + str(78))
print(str(solve([3,2,1], 2025)) + " == " + str(438))
print(str(solve([3,1,2], 2025)) + " == " + str(183))
print("answer is: " + str(solve([7,12,1,0,16,2])))

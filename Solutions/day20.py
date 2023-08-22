from os import path
from copy import deepcopy
from itertools import cycle

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

# Open and prepare input
def get_input():
    with open(path.join(data_folder, "day20.txt"), "r") as file:
        content = file.readlines()
    
    return [(idx, int(i)) for idx, i in enumerate(content)]

def part1() -> int:
    # Part 1 of the puzzle
    original = get_input()
    mixed = deepcopy(original)
    for (idx, i) in mixed:
        if i == 0:
            zero = (idx,i)
            break
    
    l = len(original) - 1

    # Shuffle
    for i in original:
        # print(mixed)
        pos = mixed.index(i)
        # print(f"{i} is in position {pos}")
        mixed.remove(i)
        new_pos = (pos + i[1] + l) % l
        # print(f"{i} should now be at {new_pos}")
        mixed.insert(new_pos, i)
    
    # Find 0 and start counting
    zero_index = mixed.index(zero)
    mixeds = mixed * 500
    return [mixeds[zero_index + 1000][1], mixeds[zero_index + 2000][1], mixeds[zero_index + 3000][1]]

def part2() -> int:
    # Part 2 of the puzzle
    dec_key = 811589153

    original = get_input()

    # The new list has every number multiplied with the decryption key
    mixed = [(idx, i * dec_key) for idx, i in original]
    original_cycle = cycle(deepcopy(mixed))
    for (idx, i) in mixed:
        if i == 0:
            zero = (idx,i)
            break

    l = len(original) - 1


    for _ in range(len(original) * 10):
        i = next(original_cycle)
        pos = mixed.index(i)
        mixed.remove(i)
        new_pos = (pos + i[1] + l) % l
        mixed.insert(new_pos, i)
    
    # Find 0 and start counting
    zero_index = mixed.index(zero)

    # Elongation of list is a lazy way of having enough space; would be better to cycle
    mixeds = mixed * 500
    return [mixeds[zero_index + 1000][1], mixeds[zero_index + 2000][1], mixeds[zero_index + 3000][1]]

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")
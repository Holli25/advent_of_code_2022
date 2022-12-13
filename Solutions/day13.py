from os import path
from typing import List

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

# Open and prepare input
def get_input():
    with open(path.join(data_folder, "day13.txt"), "r") as file:
        # eval may be unsafe, but it is soo easy to parse the input here
        pairs = [[eval(item) for item in pair.splitlines()] for pair in file.read().split("\n\n")]
        return pairs

def check_pair_sorted(pair:List[List]) -> int:
    # Function that checks if pairs are sorted according to day 13 rules
    amount_of_lists = sum(list(map(lambda x: isinstance(x, list), pair)))
    item1, item2 = pair

    # Integer comparison is left should be smaller than right; if they are equal, the next thing should be compared -> -1
    if amount_of_lists == 0:
        if item1 < item2:
            return 1
        elif item1 == item2:
            return -1
        else:
            return 0

    # If int is compared with a list: make the int to a list and compared them as two lists
    elif amount_of_lists == 1:
        if isinstance(item1, list):
            return check_pair_sorted([item1, [item2]])
        else:
            return check_pair_sorted([[item1], item2])

    elif amount_of_lists == 2:
        # If the first list is empty it means it ran out first -> sorted correctly
        if len(item1) == 0:
            return 1
        
        # If the first list still has values but the second does not it means it ran out second -> sorted incorrectly
        elif len(item2) == 0:
            return 0

        # If both lists are the same, they next item should be comopared -> -1
        elif item1 == item2:
            return -1

        # Loop only over the first list, so we know we are in bounds of first list
        for idx in range(len(item1)):
            # If second list is at an end -> sorted incorrectly
            if idx == len(item2):
                return 0

            # Pairwise comparison, if the result is either correct or incorrect, return it; otherwise continue with the next elements
            result = check_pair_sorted([item1[idx], item2[idx]])
            if result != -1:
                return result
        return 1

def merge_sort(items:List) -> List:
    # Basic merge sort
    if len(items) <= 1:
        return items
    middle = len(items)//2
    left, right = items[:middle], items[middle:]

    left = merge_sort(left)
    right = merge_sort(right)

    return custom_merge(left, right)

def custom_merge(left:List, right:List) -> List:
    # Merge function that was changed slightly so it uses the pair sorting function
    output = []
    while left and right:
        if check_pair_sorted([left[0], right[0]]) == 1:
            output.append(left[0])
            left = left[1:]
        else:
            output.append(right[0])
            right = right[1:]
    
    if not left:
        output.extend(right)
    elif not right:
        output.extend(left)
    return output

def part1() -> int:
    # Part 1 of the puzzle
    pairs = get_input()
    return sum([idx for idx, pair in enumerate(pairs, 1) if check_pair_sorted(pair)])

def part2() -> int:
    # Part 2 of the puzzle
    pairs = get_input()

    # Flatten the list, so it is not in pairs anymore, and add the markers [[2]] and [[6]]
    items = [item for pair in pairs for item in pair]
    items.append([[2]])
    items.append([[6]])

    # Sort the items, then return the positions of the markers; 1 is added as list is 0-indexed and solution wants 1-indexed
    items = merge_sort(items)
    return((items.index([[2]]) + 1) * (items.index([[6]]) + 1))

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")
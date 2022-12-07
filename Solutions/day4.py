from os import path
from typing import List, Tuple

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

def get_input() -> List[List[Tuple[str]]]:
    with open(path.join(data_folder, "day4.txt"), "r") as file:
        pairs = [line.strip().split(",") for line in file]
        pairs = [[tuple(int(section) for section in assignment.split("-")) for assignment in pair] for pair in pairs]
        return pairs

def is_overlap(pair: List[Tuple[str]], second_part_mode:bool = False) -> bool:
    # Returns True if the one assignment is fully covered by the other assignment in a pair
    # Checks whether the intersection (values both assignments have in common) is the same length as the smaller assignment; only true if the smaller assignment is fully covered by the larger assignment
    assignment_1 = set(range(pair[0][0], pair[0][1] + 1))
    assignment_2 = set(range(pair[1][0], pair[1][1] + 1))

    if second_part_mode:
        return len(assignment_1 & assignment_2) > 0

    if len(assignment_1) > len(assignment_2):
        return len(assignment_1 & assignment_2) == len(assignment_2)
    else:
        return len(assignment_1 & assignment_2) == len(assignment_1)

def part1() -> int:
    pairs = get_input()
    score = sum([is_overlap(pair) for pair in pairs])
    return score

def part2() -> int:
    pairs = get_input()
    score = sum([is_overlap(pair, second_part_mode = True) for pair in pairs])
    return score

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")
from os import path
from typing import List, Tuple

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

# Open and prepare input
def get_input():
    with open(path.join(data_folder, "day14.txt"), "r") as file:
        instructions = file.read().splitlines()
        rock:List[Tuple[int]] = []

        for line in instructions:
            line_split = line.split(" -> ")
            points = []
            for point in line_split:
                s,e = point.split(",")
                points.append((int(s), int(e)))
            for idx in range(len(points) - 1):
                start, end = points[idx], points[idx + 1]
                if start[0] - end[0] != 0:
                    if start[0] > end[0]:
                        for i in range(start[0] - end[0] + 1):
                            rock.append((end[0] + i, end[1]))
                    else:
                        for i in range(end[0] - start[0] + 1):
                            rock.append((start[0] + i, end[1]))
                else:
                    if start[1] > end[1]:
                        for i in range(start[1] - end[1] + 1):
                            rock.append((end[0], end[1] + i))
                    else:
                        for i in range(end[1] - start[1] + 1):
                            rock.append((start[0], start[1] + i))        
        return rock
       
def count_possible_sand(rock:List[Tuple[int]]) -> int:
    sands = []

    sand_possible = True
    while sand_possible:
        sand_possible, sands = simulate_next_sand(rock, sands)
        # print(f"New sand inserted at {sands[-1]}")

    return len(sands)

def count_possible_sand_2(rock:List[Tuple[int]]) -> int:
    sands = [(500,0)]
    lower_bound = max(rock, key = lambda x: x[1])[1] + 2
    for y in range(lower_bound):
        for x in range(500 - y, 500 + y + 1):
            position_taken = (x,y) in rock or (x,y) in sands
            if not position_taken:
                if (x-1,y-1) in rock and (x,y-1) in rock and (x+1,y-1) in rock:
                    pass
                elif (x-1,y-1) not in sands and (x,y-1) not in sands and (x+1,y-1) not in sands:
                    pass
                else:
                    sands.append((x,y))
    return len(sands)
    
def simulate_next_sand(rock:List[Tuple[int]], sands:List[Tuple[int]]):
    position = (500,0)
    lowest = max(rock, key = lambda x: x[1])[1]

    while True:
        if position[1] > lowest:
            return (False, sands)
        test_left, test_down, test_right = [(position[0] + i, position[1] + 1) for i in range(-1,2)]
        if test_down in rock or test_down in sands:
            if test_left in rock or test_left in sands:
                if test_right in rock or test_right in sands:
                    sands.append(position)
                    return (True, sands)
                else:
                    position = test_right
            else:
                position = test_left
        else:
            position = test_down

def simulate_next_sand_2(rock:List[Tuple[int]], sands:List[Tuple[int]]):
    position = (500,0)

    while True:
        test_left, test_down, test_right = [(position[0] + i, position[1] + 1) for i in range(-1,2)]
        if test_down in rock or test_down in sands:
            if test_left in rock or test_left in sands:
                if test_right in rock or test_right in sands:
                    sands.append(position)
                    if position == (500,0):
                        return (False, sands)
                    return (True, sands)
                else:
                    position = test_right
            else:
                position = test_left
        else:
            position = test_down

def part1() -> int:
    # Part 1 of the puzzle
    rock = get_input()
    return count_possible_sand(rock)


def part2() -> int:
    # Part 2 of the puzzle
    rock = get_input()
    # for i in range(left, right):
    #     rock.append((i, lower_bound))
    sands = count_possible_sand_2(rock)
    return sands

if __name__ == "__main__":
    # print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}") # 28037 too high
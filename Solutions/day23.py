from os import path
from typing import Dict, List, Tuple
from itertools import cycle

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

# Adjacent position movements in the order North, South, West, East
DIRECTIONS = [[(-1,-1), (0,-1), (1,-1)], [(-1,1), (0,1), (1,1)], [(-1,-1), (-1,0), (-1,1)], [(1,-1), (1,0), (1,1)]]

def add_coordinates(coord1:Tuple[int], coord2:Tuple[int]) -> Tuple[int]:
    return tuple(c1 + c2 for c1, c2 in zip(coord1, coord2))

def shuffle_directions() -> None:
    global DIRECTIONS
    DIRECTIONS = DIRECTIONS[1:] + DIRECTIONS[0:1]

def elf_moves(elf_position:Tuple[int], elves:List[Tuple[int]]) -> bool:
    for change in [(-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1)]:
        if add_coordinates(elf_position, change) in elves:
            return True
    return False

def direction_possible(elf_position:Tuple[int], directions:List[Tuple[int]], elves:List[Tuple[int]]) -> bool:
    for direction in directions:
        position = add_coordinates(elf_position, direction)
        if position in elves:
            return False
    return True

# Open and prepare input
def get_input() -> List[Tuple[int]]:
    with open(path.join(data_folder, "day23.txt"), "r") as file:
        content = file.readlines()
    return [(x,y) for y, line in enumerate(content) for x, symbol in enumerate(line) if symbol == "#"]

def part1() -> int:
    # Part 1 of the puzzle
    elves = get_input()
    elves = {i:elf for i, elf in enumerate(elves)}

    # cols = [position[0] for position in elves.values()]
    # rows = [position[1] for position in elves.values()]
    # for i in range(min(rows), max(rows) + 1):
    #     out = []
    #     for j in range(min(cols), max(cols) + 1):
    #         if (j,i) in elves.values():
    #             out.append("#")
    #         else:
    #             out.append(".")
    #     print("".join(out))

    for q in range(10):
        
        # print()
        print(f"Round {q}")
        wishes = {}
        seen = set()
        double = []

        # Go over each elf
        # Check if any directions works
        # Add wish to wishlist
        for elf_id, position in elves.items():
            if elf_moves(position, elves.values()):
                for direction in DIRECTIONS:
                    if direction_possible(position, direction, elves.values()):
                        new_coordinates = add_coordinates(position, direction[1])
                        if new_coordinates not in seen:
                            seen.add(new_coordinates)
                            wishes[elf_id] = new_coordinates
                        else:
                            double.append(new_coordinates)
                        break
        
        for elf_id, wish in wishes.items():
            if wish not in double:
                elves[elf_id] = wish

        shuffle_directions()

        # cols = [position[0] for position in elves.values()]
        # rows = [position[1] for position in elves.values()]
        # width = (max(cols) - min(cols) + 2) if max(cols) != 0 and min(cols) != 0 else (max(cols) - min(cols) + 1)
        # height = (max(rows) - min(rows) + 2) if max(rows) != 0 and min(rows) != 0 else (max(rows) - min(rows) + 1)
        # for i in range(min(rows), max(rows) + 1):
        #     out = []
        #     for j in range(min(cols), max(cols) + 1):
        #         if (j,i) in elves.values():
        #             out.append("#")
        #         else:
        #             out.append(".")
        #     print("".join(out))
    cols = [position[0] for position in elves.values()]
    rows = [position[1] for position in elves.values()]
    width = (max(cols) - min(cols) + 1)
    height = (max(rows) - min(rows) + 1)
    
    print(width, height, len(elves))

    return (width * height) - len(elves)



def part2() -> int:
    # Part 2 of the puzzle
    elves = get_input()
    elves = {i:elf for i, elf in enumerate(elves)}

    for q in range(10000):
        
        wishes = {}
        seen = set()
        double = []
        moved = 0

        # Go over each elf
        # Check if any directions works
        # Add wish to wishlist
        for elf_id, position in elves.items():
            if elf_moves(position, elves.values()):
                for direction in DIRECTIONS:
                    if direction_possible(position, direction, elves.values()):
                        new_coordinates = add_coordinates(position, direction[1])
                        if new_coordinates not in seen:
                            seen.add(new_coordinates)
                            wishes[elf_id] = new_coordinates
                        else:
                            double.append(new_coordinates)
                        break
        
        for elf_id, wish in wishes.items():
            if wish not in double:
                elves[elf_id] = wish
                moved += 1

        shuffle_directions()
        print(f"Round {q}, Moved: {moved}")
        if not moved:
            return q + 1

    cols = [position[0] for position in elves.values()]
    rows = [position[1] for position in elves.values()]
    width = (max(cols) - min(cols) + 1)
    height = (max(rows) - min(rows) + 1)
    
    print(width, height, len(elves))

    return (width * height) - len(elves)

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")
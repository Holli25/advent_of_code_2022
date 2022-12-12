from os import path
from typing import List, Tuple

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

PATHS = []

# Open and prepare input
def get_input() -> Tuple[List[str], int, int]:
    with open(path.join(data_folder, "day12.txt"), "r") as file:
        content = file.read().splitlines()
        x, y = len(content[0]), len(content)
        height_map:List[str] = [height for line in content for height in line]
        return height_map, x, y

def move_to_end(start, end, x, height_map, seen, path_length) -> bool:
    height:int = ord("a") if height_map[start] == "S" else ord(height_map[start])
    seen[start] = 1
    path_length = path_length + 1

    if start == end:
        print(f"Found path with length {path_length}")
        PATHS.append(path_length)
    elif path_length > min(PATHS):
        pass
    else:
        possible_moves = [new_position for new_position in [start+1, start+x, start-1, start-x] if new_position >= 0 and new_position < len(height_map) and ord(height_map[new_position]) - height <= 1 and seen[new_position] == 0]
        if possible_moves:
            for move in possible_moves:
                move_to_end(move, end, x, height_map, seen, path_length)
    seen[start] = 0

def move_astar(height_map, start):
    max_length = len(height_map)
    distances = []
    previous = []
    Q = []
    for idx, point in enumerate(height_map):
        distances.append(max_length)
        previous.append(max_length)
        Q.append(point)


def part1() -> int:
    # Part 1 of the puzzle
    height_map, x, y = get_input()
    start, end = height_map.index("S"), height_map.index("E")
    height_map[end] = "z"
    seen = [0 for _ in height_map]
    PATHS.append(len(height_map))
    move_to_end(start, end, x, height_map, seen, -1)
    print(PATHS)
    print(min(PATHS))

def part2() -> int:
    # Part 2 of the puzzle
    pass

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")
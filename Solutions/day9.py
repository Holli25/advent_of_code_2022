from os import path
from typing import List, Tuple

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

# Move instructions for tail based on head position
MOVE_LIST = {(2,0):(1,0), (2,1):(1,1), (1,2):(1,1), (0,2):(0,1), (-1,2):(-1,1), (-2,1):(-1,1), (-2,0):(-1,0), (-2,-1):(-1,-1), (-1,-2):(-1,-1), (0,-2):(0,-1), (1,-2):(1,-1), (2,-1):(1,-1), (2,2):(1,1), (-2,2):(-1,1), (-2,-2):(-1,-1), (2,-2):(1,-1)}
MOVES = {"R":[1,0], "L":[-1,0], "U":[0,-1], "D":[0,1]}

def list_sum(list1:List[int], list2:List[int]) -> List[int]:
    # Function sums two lists element-wise
    return [i+j for i,j in zip(list1, list2)]

def list_subtract(list1:List[int], list2:List[int]) -> List[int]:
    # Function subtracts two lists element-wise
    return [i-j for i,j in zip(list1, list2)]

# Open and prepare input
def get_input() -> List[Tuple[str, int]]:
    with open(path.join(data_folder, "day9.txt"), "r") as file:
        lines = file.read().splitlines()
        instructions = []
        for line in lines:
            direction, amount = line.split(" ")
            instructions.append((direction, int(amount)))
        return instructions

def moves(instructions) -> int:
    # Function does every move in the instructions
    # Create empty field to mark where the tail has been and initialize head and tail in the middle
    field = [[0] * 500 for _ in range(500)]
    head, tail = [250,250], [250,250]

    for move in instructions:
        for _ in range(move[1]):
            # Move the head based on the instructions
            head = list_sum(head, MOVES.get(move[0]))

            # Move the tail based on head position
            tail = move_tail(head, tail)
            field[tail[1]][tail[0]] = 1
    return sum([sum(row) for row in field])

def moves_long_rope(instructions) -> int:
    # Function does every move in the instructions
    # Create empty field to mark where the tail has been and initialize the rope in the middle with knots stacked on each other
    field = [[0] * 500 for _ in range(500)]
    rope = [[250,250] for _ in range(10)]

    for move in instructions:
        for _ in range(move[1]):
            # Move the knots; go through list and move the knot based on the knot before it, move the first knot based on the intended move
            rope = [move_tail(rope[idx - 1], knot) if idx > 0 else list_sum(knot, MOVES.get(move[0])) for idx, knot in enumerate(rope)]

            # Mark the current spot the last knot is in in the field, with 10 knots the last one has index 9
            field[rope[9][1]][rope[9][0]] = 1
    
    return sum([sum(row) for row in field])

def move_tail(head:List[int], tail:List[int]) -> List[int]:
    # Function returns the moved tail according to the current head position; only moves if needed
    separation = tuple(list_subtract(head, tail))
    tail_move = MOVE_LIST.get(separation, (0,0))
    return list_sum(tail, tail_move)


def part1() -> int:
    # Part 1 of the puzzle
    instructions = get_input()
    return moves(instructions)

def part2() -> int:
    # Part 2 of the puzzle
    instructions = get_input()
    return moves_long_rope(instructions)

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")
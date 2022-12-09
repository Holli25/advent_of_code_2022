from os import path
from typing import List, Tuple

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

# Move instructions for tail based on head position
MOVE_LIST = {(2,0):(1,0), (2,1):(1,-1), (1,2):(1,-1), (0,2):(0,-1), (-1,2):(-1,-1), (-2,1):(-1,-1), (-2,0):(-1,0), (-2,-1):(-1,1), (-1,-2):(-1,1), (0,-2):(0,1), (1,-2):(1,1), (2,-1):(1,1), (2,2):(1,-1), (-2,2):(-1,-1), (-2,-2):(-1,1), (2,-2):(1,1)}

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

    # Create empty field to mark where the tail has been and initialized head and tail in the middle
    field = [[0] * 500 for _ in range(500)]
    hx,hy = 250,250
    tx,ty = 250,250

    for move in instructions:
        # Move the head based on the instructions
        for _ in range(move[1]):
            if move[0] == "R":
                hx += 1
            elif move[0] == "L":
                hx -= 1
            elif move[0] == "U":
                hy -= 1
            elif move[0] == "D":
                hy += 1
            else:
                print("Something is messed up!")

            # Move the tail based on head position
            tx,ty = move_tail(hx, hy, tx, ty)
            field[ty][tx] = 1
            # print(field)
    return sum([sum(row) for row in field])

def moves_long_rope(instructions) -> int:
    # Function does every move in the instructions

    # Create empty field to mark where the tail has been and initialized head and tail in the middle
    field = [[0] * 500 for _ in range(500)]
    rope = [[250,250] for _ in range(10)]
    # hx,hy = 250,250
    # tx,ty = 250,250

    for move in instructions:
        # Move the head based on the instructions
        for _ in range(move[1]):
            if move[0] == "R":
                rope[0][0] += 1
            elif move[0] == "L":
                rope[0][0] -= 1
            elif move[0] == "U":
                rope[0][1] -= 1
            elif move[0] == "D":
                rope[0][1] += 1
            else:
                print("Something is messed up!")

            # Move the tail based on head position
            for knot_number in range(1,10):
                hx, hy = rope[knot_number - 1]
                rope[knot_number] = move_tail(hx, hy, rope[knot_number][0], rope[knot_number][1])
                if knot_number == 9:
                    field[rope[knot_number][1]][rope[knot_number][0]] = 1
    
    return sum([sum(row) for row in field])

def move_tail(hx:int, hy:int, tx:int, ty:int) -> Tuple[int]:
    # Function moves the tail according to the current head position
    separation = (hx-tx, ty-hy)
    x, y = MOVE_LIST.get(separation, (0,0))
    return (tx + x, ty + y)


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
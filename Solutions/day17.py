from os import path
from typing import List, Iterable
from itertools import cycle

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

# Open and prepare input
def get_input() -> Iterable[List[str]]:
    with open(path.join(data_folder, "day17.txt"), "r") as file:
        content = file.read()
        print(content)
        return cycle(["l" if i == "<" else "r" for i in content.strip()])
    
def get_pieces() -> Iterable[List[List[List[int]]]]:
    piece1 = [[0,0,1,1,1,1,0]]
    piece2 = [[0,0,0,1,0,0,0], [0,0,1,1,1,0,0], [0,0,0,1,0,0,0]]
    piece3 = [[0,0,1,1,1,0,0], [0,0,0,0,1,0,0], [0,0,0,0,1,0,0]]
    piece4 = [[0,0,1,0,0,0,0], [0,0,1,0,0,0,0], [0,0,1,0,0,0,0], [0,0,1,0,0,0,0]]
    piece5 = [[0,0,1,1,0,0,0], [0,0,1,1,0,0,0]]
    return cycle([piece1, piece2, piece3, piece4, piece5])

def display_stack(stack:List[List[int]]) -> None:
    # Utility function to display the current stack
    # Stack is in reverse order
    for row in stack[::-1]:
        out = "".join(["#" if i else "." for i in row])
        print(f"|{out}|")
    print("+-------+")

def add_rows(row1:List[int], row2:List[int]) -> List[int]:
    # Bitwise summation of two rows
    return [r1 + r2 for r1, r2 in zip(row1, row2)]

def move_in_bounds(piece:List[List[int]], flow:str) -> bool:
    # Checks if the current move is in bounds
    left_bound = min([row.index(1) for row in piece if row.count(1) >= 1])
    right_bound = 6 - min([row[::-1].index(1) for row in piece if row.count(1) >= 1])
    if flow == "l":
        return left_bound - 1 >= 0
    else:
        return right_bound + 1 <= 6
    
def prune_stack(stack:List[List[int]]) -> List[List[int]]:
    # Removes all lines from the top of the stack, that are completely empty
    while True:
        if sum(stack[-1]) > 0:
            break
        stack.pop()
    return stack

def move(piece:List[List[int]], flow:str) -> List[List[int]]:
    if flow == "l":
        return [row[1:] + [0] for row in piece]
    else:
        return [[0] + row[:-1] for row in piece]
    
def move_possible(piece:List[List[int]], substack:List[List[int]]) -> bool:
    for p, s in zip(piece, substack):
        if max(add_rows(p, s)) > 1:
            return False
    return True

def advance_stack(stack, piece, j):
    if j == 0:
        return stack + piece
    elif j <= len(piece):
        return stack[:-j] + [add_rows(stack[-j+a], piece[a]) for a in range(j)] + piece[j:]
    elif len(stack) < len(piece):
        return [[add_rows(stack[-a], piece[a]) for a in range(len(stack))]] + piece[len(stack):]
    else:
        stack_end = j - len(piece)
        return stack[:-j] + [add_rows(stack[-j+a], piece[a]) for a in range(len(piece))] + stack[-stack_end:]

def part1() -> int:
    # Part 1 of the puzzle
    flows = get_input()
    pieces = get_pieces()
    stack = []
    for i,p in enumerate(pieces):
        # Move the piece according to the jet flows; always 4, as only then will it reach the current top
        for _ in range(4):
            flow = next(flows)
            if move_in_bounds(p, flow):
                p = move(p, flow)
        
        # Leave the loop when we are at the 2023th stone
        if i == 2022:
            break

        # First flat piece will be the stack
        if i == 0:
            stack = p
        else:
            j = 1
            # After the jet stream, the piece falls down one if possible. If not, it will be settled/added to the stack
            while move_possible(p, stack[-j:]):
                flow = next(flows)
                if move_in_bounds(p, flow) and move_possible(move(p, flow), stack[-j:]):
                    p = move(p, flow)
                
                # Special case, where the piece is bigger than the stack, need to add to j first, so it is the correct size after reducing it again
                if j == len(stack):
                    j += 1
                    break
                j += 1
                
            j -= 1
            # i == print(f"Round: {i}, went down {j}")
            stack = advance_stack(stack, p, j)
            if i == 2:
                display_stack(stack)

    print(len(stack))
    

def part2() -> int:
    # Part 2 of the puzzle
    pass

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    # print(f"Solution to Part2: {part2()}")
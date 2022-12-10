from os import path
from typing import List

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

# Create global variables for screen and line of screen
SCREEN:List[List[str]] = []
LINE:List[str] = []

# Open and prepare input
def get_input():
    with open(path.join(data_folder, "day10.txt"), "r") as file:
        instructions = [line for line in file.read().splitlines()]
        return instructions

def run_instructions(instructions: List[str]) -> int:
    # Function goes up to cycle 241 and changes the register and signal strength accordingly
    # Signal strength is only updated after cycle 20,60,100,140,180,220
    cycle:int = 0
    x:int = 1
    signal_strength:int = 0

    for instruction in instructions:
        # noop just changes the cycle by 1
        if instruction == "noop":
            cycle += 1
            if cycle in [20,60,100,140,180,220]:
                signal_strength += cycle * x
        else:
            # Additions take two cycles to take effect, register is updated at the end of the cycle
            for _ in range(2):
                cycle += 1
                if cycle in [20,60,100,140,180,220]:
                    signal_strength += cycle * x
            # Format is 'addx y' with y being the amount to change the register
            amount = int(instruction.split("addx ")[1])
            x += amount
        # Stop after cycle 220, as the signal strength is only calculated until then
        if cycle > 220:
            break
    return signal_strength

def update_screen(cycle:int, register:int) -> None:
    # Creates the current line and adds it to the screen if full
    global LINE, SCREEN
    sprite:List[int] = [register-1,register,register+1]
    LINE.append('#') if cycle % 40 in sprite else LINE.append(".")
    if len(LINE) >= 40:
        SCREEN.append(LINE)
        LINE = []

def draw_screen(instructions: List[str]) -> None:
    # Function goes until cycle 241 and updates the screen accordinly
    cycle:int = 0
    x:int = 1

    for instruction in instructions:
        # noop just changes the cycle by 1
        if instruction == "noop":
            update_screen(cycle, x)
            cycle += 1   
        else:
            # Additions take two cycles to take effect, register is updated at the end of the cycle
            for _ in range(2):
                update_screen(cycle, x)
                cycle += 1
            # Format is 'addx y' with y being the amount to change the register
            amount = int(instruction.split("addx ")[1])
            x += amount
        if cycle > 240:
            break
    for line in SCREEN:
        print("".join(line))

def part1() -> int:
    # Part 1 of the puzzle
    instructions = get_input()
    return run_instructions(instructions)

def part2() -> int:
    # Part 2 of the puzzle
    instructions = get_input()
    draw_screen(instructions)

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print("Solution to Part2 is:")
    part2()
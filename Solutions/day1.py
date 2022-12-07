from os import path

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

# Open input, split by empty new line; then sum all calories for each elf
with open(path.join(data_folder, "day1.txt"), "r") as file:
    content = file.read()
    elf_food = content.split("\n\n")
    elf_calories = [sum([int(calory) for calory in elf.split("\n")]) for elf in elf_food]

def part1() -> int:
    # Part 1 of the puzzle
    return(max(elf_calories))

def part2() -> int:
    # Part 2 (sort the calories by amount and only get the top 3, then sum them up)
    elf_calories.sort()
    return(sum(elf_calories[-3:]))   

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")
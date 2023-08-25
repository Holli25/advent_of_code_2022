from os import path
from re import findall
from typing import Dict, Tuple

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

# Open and prepare input
def get_input():
    with open(path.join(data_folder, "day21.txt"), "r") as file:
        content = file.read()
        operation_monkeys = findall("(\w{4}): (\w{4}) ([\+\-\*\/]) (\w{4})", content)
        number_monkeys = findall("(\w{4}): (\d+)", content)
        return operation_monkeys, number_monkeys

def calculate_monkey_number(operation_monkey:Tuple[str], monkey_numbers:Dict[str, int]) -> int:
    if operation_monkey[2] == "+":
        return monkey_numbers[operation_monkey[1]] + monkey_numbers[operation_monkey[3]]
    elif operation_monkey[2] == "-":
        return monkey_numbers[operation_monkey[1]] - monkey_numbers[operation_monkey[3]]
    elif operation_monkey[2] == "*":
        return monkey_numbers[operation_monkey[1]] * monkey_numbers[operation_monkey[3]]
    elif operation_monkey[2] == "/":
        return monkey_numbers[operation_monkey[1]] // monkey_numbers[operation_monkey[3]]
    print("Something was messed up!")
    return 0

def calculate_monkey_number_part2(goal_monkey_info:Tuple[str], goal_monkey_number:int, side_monkey_number:int, side_monkey_name:str) -> Tuple[str, int]:
    new_goal_monkey = goal_monkey_info[1] if not goal_monkey_info[1] == side_monkey_name else goal_monkey_info[3]

    # Root operation is equal
    if goal_monkey_info[0] == "root":
        return (new_goal_monkey, side_monkey_number)

    # + is a commutative operation, goal_monkey_number is always bigger than both side_monkey_numbers
    if goal_monkey_info[2] == "+":
        return (new_goal_monkey, goal_monkey_number - side_monkey_number)
    # - is NOT a commutative operation, so we have to know the order
    elif goal_monkey_info[2] == "-":
        if new_goal_monkey == goal_monkey_info[1]:
            return (new_goal_monkey, goal_monkey_number + side_monkey_number)
        else:
            return (new_goal_monkey, side_monkey_number - goal_monkey_number)
    # * is a commutative operation 
    elif goal_monkey_info[2] == "*":
        return (new_goal_monkey, goal_monkey_number // side_monkey_number)
    # / is NOT a commutative operation, so we have to know the order
    elif goal_monkey_info[2] == "/":
        if new_goal_monkey == goal_monkey_info[1]:
            return (new_goal_monkey, goal_monkey_number * side_monkey_number)
        else:
            return (new_goal_monkey, side_monkey_number // goal_monkey_number)

def get_comparison_value(operation_monkeys, number_monkeys, goal_monkey) -> Tuple[int, int]:
    operation_monkeyss = {monkey[0]:monkey for monkey in operation_monkeys}

    for side in [1,3]:
        monkey_numbers = {monkey:int(number) for monkey, number in number_monkeys}
        # print(operation_monkeyss, goal_monkey)
        if not operation_monkeyss.get(goal_monkey)[side]:
            print("It happened!! The monkey is no operation monkey")
        side_goal = operation_monkeyss.get(goal_monkey)[side]
        side_monkeys = []
        open = [side_goal]
        while open:
            c = open.pop(0)
            side_monkeys.append(c)
            if c in operation_monkeyss:
                open.append(operation_monkeyss.get(c)[1])
                open.append(operation_monkeyss.get(c)[3])
        if "humn" in side_monkeys:
            continue
        while not side_monkeys[0] in monkey_numbers:
            for monkey in [monkey for monkey in operation_monkeyss.values()]:
                if monkey[0] in side_monkeys and monkey[1] in monkey_numbers and monkey[3] in monkey_numbers:
                    number = calculate_monkey_number(monkey, monkey_numbers)
                    operation_monkeys.remove(monkey)
                    del operation_monkeyss[monkey[0]]
                    monkey_numbers[monkey[0]] = number
        break
    return (monkey_numbers.get(operation_monkeyss.get(goal_monkey)[side]), operation_monkeyss.get(goal_monkey)[side])

def part1() -> int:
    # Part 1 of the puzzle
    operation_monkeys, number_monkeys = get_input()
    monkey_numbers = {monkey:int(number) for monkey, number in number_monkeys}
    while not "root" in monkey_numbers:
        for monkey in operation_monkeys:
            if monkey[1] in monkey_numbers and monkey[3] in monkey_numbers:
                number = calculate_monkey_number(monkey, monkey_numbers)
                operation_monkeys.remove(monkey)
                monkey_numbers[monkey[0]] = number
                print(f"Monkey {monkey[0]} now has {number}")
    return monkey_numbers["root"]

def part2() -> int:
    # Part 2 of the puzzle
    operation_monkeys, number_monkeys = get_input()
    operation_monkeyss = {monkey[0]:monkey for monkey in operation_monkeys}

    # Remove the human as a number, as our number is the puzzle answer
    for nm in number_monkeys:
        if nm[0] == "humn":
            break
    number_monkeys.remove(nm)
    goal_monkey_name = "root"
    final_number = 0

    # Calculate the number upstream of humn
    while "humn" not in operation_monkeyss.get(goal_monkey_name):
        side_monkey_number, side_monkey = get_comparison_value(operation_monkeys, number_monkeys, goal_monkey_name)
        goal_monkey_name, final_number = calculate_monkey_number_part2(goal_monkey_info=operation_monkeyss.get(goal_monkey_name), goal_monkey_number=final_number, side_monkey_number=side_monkey_number, side_monkey_name=side_monkey)
        
    # Calculate the number next to humn
    side_monkey = operation_monkeyss.get(goal_monkey_name)[1] if operation_monkeyss.get(goal_monkey_name)[1] != "humn" else operation_monkeyss.get(goal_monkey_name)[3]
    
    monkey_numbers = {monkey:int(number) for monkey, number in number_monkeys}
    while not side_monkey in monkey_numbers:
        for monkey in operation_monkeys:
            if monkey[1] in monkey_numbers and monkey[3] in monkey_numbers:
                number = calculate_monkey_number(monkey, monkey_numbers)
                operation_monkeys.remove(monkey)
                monkey_numbers[monkey[0]] = number
    side_monkey_number = monkey_numbers.get(side_monkey)

    goal_monkey_name, final_number = calculate_monkey_number_part2(goal_monkey_info=operation_monkeyss.get(goal_monkey_name), goal_monkey_number=final_number, side_monkey_number=side_monkey_number, side_monkey_name=side_monkey)
    return final_number

    

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")
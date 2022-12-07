from os import path
from typing import List, Tuple

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

# Open and prepare input
def get_input() -> Tuple[List[List[str]], List[Tuple[int]]]:
    with open(path.join(data_folder, "day5.txt"), "r") as file:
        content = file.read()
        configuration, moves = content.split("\n\n") # Split by double new line, as this separates the starting configuration and the move instructions

        ## Prepare the configuration
        # Last column ends with [x] and does not have a trailing whitespace, so if 3 are deducted from the total length, each column has a length of 4; then we add the last column to that number
        # Create a list for each column: Get the cargo in reverse order (first in list is most bottom on stack)
        # [4 * column + 1] yields the cargo in the [x] [y] [z] format, as each cargo is separated by 4 strings
        # To get reverse order, rows[-2::-1] is used, -2 to leave out the last line that only contains the column number
        rows = configuration.split("\n")
        column_amount = 1 + (len(rows[0]) - 3) // 4
        columns = [[row[4 * column + 1] for row in rows[-2::-1] if row[4 * column + 1] != " "] for column in range(column_amount)]

        ## Prepare the moves
        # Each move is in a new line -> moves.split("\n")
        # the pattern for each move is "move {number} from {number} to {number}"; splitting by " " and taking the 2nd, 4th and 6th portion yields only the numbers
        # Numbers are stored in a tuple
        moves = [(int(move.split(" ")[1]), int(move.split(" ")[3]), int(move.split(" ")[5])) for move in moves.split("\n")]

        return(columns, moves)

def move_cargo_CrateMover9000(columns: List[List[str]], moves: List[Tuple[int]]) -> List[List[str]]:
    # Move the cargo on the columns corresponding to the move instructions; cargo is moved in reverse order
    # Simple solution is to pop the element from the list and append it to the assigned new column-list
    for move in moves:
        for _ in range(move[0]):
            cargo = columns[move[1] - 1].pop()
            columns[move[2] - 1].append(cargo)
    return columns

def move_cargo_CrateMover9001(columns: List[List[str]], moves: List[Tuple[int]]) -> List[List[str]]:
    # Move the cargo on the columns corresponding to the move instructions; cargo is moved retaining the order
    # Simple solution is to slice out the needed part and remove it afterwards from the origin column
    for move in moves:
        amount, origin_column, destination_column = move[0], move[1] - 1, move[2] - 1
        cargo = columns[origin_column][len(columns[origin_column]) - amount:]
        columns[destination_column].extend(cargo)
        columns[origin_column] = columns[origin_column][:len(columns[origin_column]) - amount]
    return columns

def get_upper_cargos(columns: List[List[str]]) -> str:
    # Get the upper most cargo symbols and return them as a string
    # Only get the last element (which is the upper one) and join them
    return "".join([column[-1] for column in columns])


def part1() -> str:
    # Part 1 of the puzzle
    columns, moves = get_input()
    columns = move_cargo_CrateMover9000(columns, moves)
    return get_upper_cargos(columns)

def part2() -> str:
    # Part 2 of the puzzle
    columns, moves = get_input()
    columns = move_cargo_CrateMover9001(columns, moves)
    return get_upper_cargos(columns)

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")
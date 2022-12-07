from os import path

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

# Open and prepare input
def get_input() -> str:
    with open(path.join(data_folder, "day6.txt"), "r") as file:
        signal = file.read().rstrip()
        return signal

def detect_start(signal: str, search_length: int) -> int:
    # Detects slice of a certain size that does not contain duplicate characters
    # Create sliding windows of search_length size
    # slice with no duplicate characters is found when the set has search_length characters (no character filtered out)
    # Start is the index of the next character after the slice was found
    for possible_start in range(search_length, len(signal) + 1):
        buffer = signal[possible_start - search_length:possible_start]
        if len(set(buffer)) == search_length:
            return possible_start

def part1() -> int:
    # Part 1 of the puzzle
    # Buffer size is 4
    signal = get_input()
    return detect_start(signal, search_length = 4)

def part2() -> int:
    # Part 2 of the puzzle
    # Message size is 14
    signal = get_input()
    return detect_start(signal, search_length = 14)

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")
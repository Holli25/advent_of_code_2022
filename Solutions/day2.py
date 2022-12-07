from os import path
from typing import List

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

signs = {"A":"Rock", "B":"Paper", "C":"Scissors", "X":"Rock", "Y":"Paper", "Z":"Scissors"}
points = {"A":{"X":3, "Y":6, "Z":0}, "B":{"X":0, "Y":3, "Z":6}, "C":{"X":6, "Y":0, "Z":3}, "X":1, "Y":2, "Z":3}

signs_2 = {"A":"Rock", "B":"Paper", "C":"Scissors", "X":0, "Y":3, "Z":6}
points_2 = {"A":{3:1, 6:2, 0:3}, "B":{0:1, 3:2, 6:3}, "C":{6:1, 0:2, 3:3}}

def get_input() -> List[List[str]]:
    with open(path.join(data_folder, "day2.txt"), "r") as file:
        rounds = [line.strip().split(" ") for line in file]
        return rounds

def determine_result(round: List[str]) -> int:
    # Returns 0 for a loss, 3 for a draw and 6 for a win
    # Input: round, List with two str, first is the opponent, second is your sign
    return points.get(round[0]).get(round[1])


def calculate_round_points(round: List[str]) -> int:
    # Calculates the points of one round by adding the worth of your sign to the outcome points
    # Input: round, List with two str, first is the opponent, second is your sign
    return points.get(round[1], -100) + determine_result(round)
    
def calculate_round_points_2(round: List[str]) -> int:
    # Calculates the points of one round by adding the worth of your sign to the outcome points
    # Input: round, List with two str, first is the opponent's sign, second is the outcome
    outcome = signs_2.get(round[1], -100)
    return outcome + points_2.get(round[0]).get(outcome)

def part1() -> int:
    rounds = get_input()
    points = [calculate_round_points(round) for round in rounds]
    return sum(points)

def part2() -> int:
    rounds = get_input()
    points = [calculate_round_points_2(round) for round in rounds]
    return sum(points)

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")
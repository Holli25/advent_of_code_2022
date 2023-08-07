from os import path
from re import match, findall
from typing import Dict, List, Tuple
from copy import deepcopy

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

# Open and prepare input
def get_input() -> List[Tuple[str, int, str]]:
    with open(path.join(data_folder, "day16.txt"), "r") as file:
        content = file.read()

    pattern = "Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? ((?:\w{2}(?:, )?)+)"
    matches = findall(pattern, content)
    
    return [(name, int(flow), neighbors) for name, flow, neighbors in matches]

def create_distance_matrix(valve_info: List[Tuple[str, str]]) -> List[List[int]]:
    l = len(valve_info)
    valve_numbers = {info[0]:idx for idx, info in enumerate(valve_info)}
    matrix = [[l*l if i != j else 0 for i in range(l)] for j in range(l)]

    for cycle in range(len(matrix)):
        matrix_copy = deepcopy(matrix)

        if cycle == 0:
            for row, valve in enumerate(valve_info):
                for neighbor in valve[1].split(", "):
                    matrix[row][valve_numbers[neighbor]] = 1
        
        else:
            for valve_number in range(len(matrix_copy)):
                for neighbor_number in range(len(matrix_copy)):
                    if matrix_copy[valve_number][neighbor_number] == cycle:
                        for next_neighbor, distance in enumerate(matrix_copy[neighbor_number]):
                            if distance + cycle < matrix[valve_number][next_neighbor]:
                                matrix[valve_number][next_neighbor] = distance + cycle
        
    return matrix

def calculate_distance_to_relevant_valves(current_valve:int, distance_matrix:List[List[int]], relevant_valves:List[Tuple[int]]) -> List[int]:
    return [distance_matrix[current_valve][valve[0]] + 1 for valve in relevant_valves]

def calculate_flow_possibilities(cycles:int, distance_vector:List[int], relevant_valves:List[Tuple[int]]):
    return [(info[0], (cycles - distance) * info[1]) for distance, info in zip(distance_vector, relevant_valves)]
    
def solve(amount:int, cycle:int, current:int, relevant_valves:List[Tuple[int]], distance_matrix:List[List[int]]):
    # print(f"Cycle: {cycle}, Valve: {current}, remaining: {relevant_valves}")
        
    # Check if the current valve id is in the relevant valves (valve with possible flow)
    relevant_valve_number = -1
    for idx, valve in enumerate(relevant_valves):
        if valve[0] == current:
            relevant_valve_number = idx
            break
    
    new_relevant_valves = relevant_valves.copy()
    if relevant_valve_number >= 0:
        # print(f"Before: {amount}, flow: {relevant_valves[relevant_valve_number][1]}")
        amount = amount + cycle * relevant_valves[relevant_valve_number][1]
        # print(f"After: {amount}")
        new_relevant_valves.pop(relevant_valve_number)
    # print(amount)

    if len(new_relevant_valves) == 0:
        return amount

    flows = []

    distances = calculate_distance_to_relevant_valves(current, distance_matrix, new_relevant_valves)
    flow_possibilities = calculate_flow_possibilities(cycle, distances, new_relevant_valves)
    flow_possibilities.sort(key=lambda x: x[1], reverse=True)
    searching_valves = [valve_info[0] for idx, valve_info in enumerate(flow_possibilities) if idx < 6]

    for valve in searching_valves:
        # print(f"Origin: {current}; Destination: {valve[0]}")
        remaining_cycle = cycle - distance_matrix[current][valve] - 1
        if remaining_cycle >= 0:
            new = solve(amount, remaining_cycle, valve, new_relevant_valves, distance_matrix)
            flows.append(new)
            # print(new_relevant_valves)
    # print(f"Finished looking! Found: {flows}")
    if flows:
        return max(flows)
    else:
        return amount

def part1() -> int:
    # Part 1 of the puzzle
    valve_info = get_input()
    ford = [(name, neighbors) for name, _, neighbors in valve_info]
    distance_matrix = create_distance_matrix(ford)
    relevant_valves = [(i, info[1]) for i, info in enumerate(valve_info) if info[1] > 0]
    start = 0
    for i, valve in enumerate(valve_info):
        if valve[0] == "AA":
            start = i
            break
    print(solve(0, 30, i, relevant_valves, distance_matrix))


def part2() -> int:
    # Part 2 of the puzzle
    pass

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    # print(f"Solution to Part2: {part2()}")
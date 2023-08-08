from os import path
from typing import Dict, List

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

# Open and prepare input
def get_input():
    with open(path.join(data_folder, "day18.txt"), "r") as file:
        content = file.readlines()
        return [[int(i) for i in row.strip().split(",")] for row in content]

def free_sides_of_cube(cube:List[int], cubes:List[List[int]]) -> int:
    # Iterates over each side of the cube and checks if there is another cube
    free_sides = 0
    for change in [[-1,0,0], [1,0,0], [0,-1,0], [0,1,0], [0,0,-1], [0,0,1]]:
        if [cube[0] + change[0], cube[1] + change[1], cube[2] + change[2]] not in cubes:
            free_sides += 1
    return free_sides

def free_sides_of_cube_without_inside(cube:List[int], cubes:List[List[int]], trapped:List[List[int]]) -> int:
    # Iterates over each side of the cube and checks if there is another cube
    # If there is no cube but the position is marked as trapped, it is not on the outside
    free_sides = 0
    for dx,dy,dz in [[-1,0,0], [1,0,0], [0,-1,0], [0,1,0], [0,0,-1], [0,0,1]]:
        if [cube[0] + dx, cube[1] + dy, cube[2] + dz] not in cubes and [cube[0] + dx, cube[1] + dy, cube[2] + dz] not in trapped:
            free_sides += 1
    return free_sides

def part1() -> int:
    # Part 1 of the puzzle
    cubes = get_input()
    return sum([free_sides_of_cube(cube, cubes) for cube in cubes])


def part2() -> int:
    # Part 2 of the puzzle
    cubes = get_input()

    # Go over all positions and check if they are trapped. A trapped position is marked as not connected to the outside.
    free = [[0,0,0]]
    trapped = []
    for x in range(22):
        print(f"Started with x={x}")
        for y in range(22):
            for z in range(0,22):
                if [x,y,z] not in cubes:
                    for dx,dy,dz in [[-1,0,0], [1,0,0], [0,-1,0], [0,1,0], [0,0,-1], [0,0,1]]:
                        if [x+dx, y+dy, z+dz] in free:
                            free.append([x,y,z])
                            break
                if [x,y,z] not in free and [x,y,z] not in cubes:
                    trapped.append([x,y,z])
    
    # As the previous operation only checked in one axis (z,y), there will be positions marked as trapped which are free
    # Try to eliminate them one by one by checking whether trapped positions are in fact connected to a free position and are thus free
    before = len(trapped) + 1
    after = len(trapped)
    while before > after:
        for x,y,z in trapped:
            for dx,dy,dz in [[-1,0,0], [1,0,0], [0,-1,0], [0,1,0], [0,0,-1], [0,0,1]]:
                if [x+dx,y+dy,z+dz] in free:
                    trapped.pop(trapped.index([x,y,z]))
                    free.append([x,y,z])
                    break
        before = after
        after = len(trapped)
    return sum([free_sides_of_cube_without_inside(cube, cubes, trapped) for cube in cubes])


if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")
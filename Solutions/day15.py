from os import path
import re
from typing import Dict, List, Tuple
from collections import defaultdict

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

# Open and prepare input
def get_input() -> List[Dict[str, Tuple[int]]]:
    coord_re = re.compile(".*x=(-?[0-9]+), y=(-?[0-9]+):.*x=(-?[0-9]+), y=(-?[0-9]+)")
    with open(path.join(data_folder, "day15.txt"), "r") as file:
        scanners = []
        for line in file.read().splitlines():
            coords = coord_re.match(line)
            scanners.append({"self":(int(coords.group(1)), int(coords.group(2))), "beacon":(int(coords.group(3)), int(coords.group(4)))})
        return scanners

def part1() -> int:
    # Part 1 of the puzzle
    scanners = get_input()
    line_to_check = 2000000
    no_beacon = set()
    for i in scanners:
        s,b = i.get("self"), i.get("beacon")

        # Calculate the distance from the scanner to the beacon, x will be the remaining steps on the y coordinate that is left after going to that line
        distance = abs(s[0] - b[0]) + abs(s[1] - b[1])
        distance_to_line = abs(s[1] - line_to_check)
        x = distance - distance_to_line

        # For each possible step in both directions, add the position to the list of no possible beacons
        for j in range(-x,x):
            no_beacon.add(s[0] + j)
    print(len(no_beacon))

def convert_scanners(scanners):
    output = []
    for scanner in scanners:
        scanner_coords, beacon_coords = scanner.get("self"), scanner.get("beacon")
        distance = abs(scanner_coords[0] - beacon_coords[0]) + abs(scanner_coords[1] - beacon_coords[1])
        output.append((scanner_coords, distance))
    return output

def get_scanner_outline(scanner:Dict[str, Tuple[int]]) -> List[Tuple[int]]:
    # Function generates the sorted outline of a circle around a scanner, in which no other beacon can be based on the closest seen beacon
    # The outline is sorted clockwise starting from its highest point
    scanner_coords, beacon_coords = scanner.get("self"), scanner.get("beacon")
    sx, sy = scanner_coords

    # Manhattan distance is used in the task
    distance = abs(scanner_coords[0] - beacon_coords[0]) + abs(scanner_coords[1] - beacon_coords[1])
    outline = set()
    for x in range(-distance,distance + 1):
        y = distance - abs(x)
        outline.add((sx + x, sy + y))
        outline.add((sx + x, sy - y))

    # Sort outline by starting with the top most coordinate and then moving clockwise
    outline = sorted(list(outline), key = lambda x: x[1])
    top = outline[0]
    left = [point for point in outline if point[0] < top[0]]
    right = [point for point in outline if point[0] >= top[0]]
    outline = right + left[::-1]
    return outline

def scanners_overlap(scanner1, scanner2) -> bool:
    s1, b1 = scanner1.get("self"), scanner1.get("beacon")
    s2, b2 = scanner2.get("self"), scanner2.get("beacon")

    radius1 = abs(s1[0] - b1[0]) + abs(s1[1] - b1[1])
    radius2 = abs(s2[0] - b2[0]) + abs(s2[1] - b2[1])

    return (abs(s1[0] - s2[0]) + abs(s1[1] - s2[1])) < (radius1 + radius2)

def combine_scanner_outlines(scanner1, scanner2):
    intersection = set(scanner1).intersection(set(scanner2))
    print(len(intersection))
    s1 = sorted(list(scanner1), key = lambda x: x[0])
    s2 = sorted(list(scanner2), key = lambda x: x[0])
    if len(intersection) == 0:
        return set()
        # out = s1
        # out.extend(s2)
        # return set(out)
    a = list(intersection)[0]
    out = s1[:s1.index(a)]
    out.extend(s2[s2.index(a):])
    return set(out)


def part2() -> int:
    # Part 2 of the puzzle
    scanners = get_input()
    scanners = convert_scanners(scanners)
    print(scanners)
    # start = scanners[0]
    # start = get_scanner_outline(start)
    # no_overlap = []
    # for i in range(4, 5):
    #     new = get_scanner_outline(scanners[i])
    #     if scanners_overlap(scanners[0], scanners[i]):
    #         temp = combine_scanner_outlines(start, new)
    #     else:
    #         no_overlap.append(scanners[i])
            
    # start += new
    # for y in range(-10,30):
    #     row = ["#" if (x,y) in start else "." for x in range(-10,30)]
    #     print("".join(row))
    # new = get_scanner_outline(scanners[4])
    # for y in range(-10,30):
    #     row = ["#" if (x,y) in new else "." for x in range(-10,30)]
    #     print("".join(row))
        


if __name__ == "__main__":
    # print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")
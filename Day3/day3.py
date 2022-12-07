from typing import List, Tuple
from string import ascii_letters

def get_input(second_part: bool = False) -> List[Tuple[str]]:
    # Input is separated in two strings (cut in half) in the first part and not separated in the second
    with open("input.txt", "r") as file:
        if second_part:
            rucksacks = [line.strip() for line in file]
        else:
            rucksacks = [(line.strip()[:len(line)//2], line.strip()[len(line)//2:]) for line in file]
        return rucksacks

def find_common_element(rucksack: Tuple[str]) -> str:
    # Returns the common element of two compartments of a rucksack
    # Set intersection finds the element, list()[0] returns the element as a string
    return list(set(rucksack[0]) & set(rucksack[1]))[0]

def calculate_rucksack_priority(rucksack: Tuple[str]) -> int:
    # Returns the priority of the rucksack
    # ascii_letters are already presorted, add 1 because of 0-indexing
    common_element = find_common_element(rucksack)
    priority = ascii_letters.index(common_element) + 1
    return priority

def calculate_rucksack_priority_secondpart(rucksack1: Tuple[str], rucksack2: Tuple[str], rucksack3: Tuple[str]) -> int:
    # Returns the priority of a group of rucksacks
    # Find the common element by set intersection, list()[0] returns the element as a string
    # ascii_letters are already presorted, add 1 because of 0-indexing
    common_element = list(set(rucksack1) & set(rucksack2) & set(rucksack3))[0]
    priority = ascii_letters.index(common_element) + 1
    return priority

def part1() -> int:
    rucksacks = get_input()
    score = sum([calculate_rucksack_priority(rucksack) for rucksack in rucksacks])
    return score

def part2() -> int:
    rucksacks = get_input(second_part = True)
    score = 0
    for i in range(0, len(rucksacks), 3):
        score += calculate_rucksack_priority_secondpart(rucksack1=rucksacks[i], rucksack2=rucksacks[i+1], rucksack3=rucksacks[i+2])
    return score

print(part1())
print(part2())
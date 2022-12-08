from os import path
from typing import List

# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

# Open and prepare input
def get_input() -> List[List[int]]:
    with open(path.join(data_folder, "day8.txt"), "r") as file:
        content = file.read().splitlines()
        trees = [[int(tree) for tree in row] for row in content]
        return trees

def generate_visibility_map(trees: List[List[int]]) -> List[List[int]]:
    # Function that generates a map of the trees consisting of 1s (tree visible) and 0s (tree not visible)
    # Checks row-wise and column-wise, not the fastest way I guess

    # Create tree map with only 0s
    visible_trees = [[0] * len(trees[0]) for _ in range(len(trees))]

    # Check row-wise
    for row_idx, row in enumerate(trees):
        # Check left to right
        for col, tree in enumerate(row):
            visible = True

            # Check all trees left of the current tree, if one is equal or taller than the current tree, it is not visible
            for earlier_tree_index in range(col):
                if tree <= row[earlier_tree_index]:
                    visible = False
                    break
            if visible:
                visible_trees[row_idx][col] = 1

            # Once a tree is of size 9, all trees right of it can not be seen, so loop is broken to save time
            elif tree == 9:
                break

        # Check right to left
        for col, tree in enumerate(row[::-1]):
            visible = True

            # Check all trees right of the current tree, if one is equal or taller than the current tree, it is not visible
            for earlier_tree_index in range(col):
                if tree <= row[- earlier_tree_index - 1]:
                    visible = False
                    break
            if visible:
                visible_trees[row_idx][- col - 1] = 1

            # Once a tree is of size 9, all trees left of it can not be seen, so loop is broken to save time
            elif tree == 9:
                break
    
    for col_idx in range(len(trees[0])):
        # Check top down
        for row_idx in range(len(trees)):
            # Get the current tree
            tree = trees[row_idx][col_idx]
            visible = True

            # Check all trees higher than the current tree, if one is equal or taller than the current tree, it is not visible
            for earlier_tree_index in range(row_idx):
                if tree <= trees[earlier_tree_index][col_idx]:
                    visible = False
                    break
            if visible:
                visible_trees[row_idx][col_idx] = 1

            # Once a tree is of size 9, all lower than it can not be seen, so loop is broken to save time
            elif tree == 9:
                break

        # Check bottom up
        for row_idx in range(len(trees) - 1, -1, -1):
            # Get the current tree
            tree = trees[row_idx][col_idx]
            visible = True

            # Check all trees lower than the current tree, if one is equal or taller than the current tree, it is not visible
            for earlier_tree_index in range(row_idx + 1, len(trees)):

                # Out-of-bounds check
                if earlier_tree_index >= len(trees):
                    break
                if tree <= trees[earlier_tree_index][col_idx]:
                    visible = False
                    break
            if visible:
                visible_trees[row_idx][col_idx] = 1

            # Once a tree is of size 9, all higher than it can not be seen, so loop is broken to save time
            elif tree == 9:
                break

    return visible_trees

def get_view_score(trees: List[int], position: int, dimension: int) -> int:
    # Function calculates the view score for one tree at a marked position
    height = trees[position]

    # Horizontal
    # Get the amount of trees to the left and right
    left_index = position % dimension
    right_side = dimension - left_index

    # Slice the tree list accordingly to get only the left or right portion
    left, right = trees[position - left_index:position], trees[position + 1:position + right_side]

    # Calculate the score by leaving only trees that are smaller and stop when the first tree that is equal or higher to the current tree
    # Left side has to use reverse order so it is the viewing direction
    l_score = sum([1 for _ in takewhile_including(lambda x: x < height, left[::-1])])
    r_score = sum([1 for _ in takewhile_including(lambda x: x < height, right)])

    # Vertical
    # Slicing using the positions calculated above, bottom takes the current tree and slices it off afterwards
    top, bottom = trees[left_index:position:dimension], trees[position::dimension][1:]
    t_score = sum([1 for _ in takewhile_including(lambda x: x < height, top[::-1])])
    b_score = sum([1 for _ in takewhile_including(lambda x: x < height, bottom)])

    return l_score * r_score * t_score * b_score
    
def takewhile_including(predicate, iterable):
    """
    Alternative takewhile function from itertools; keeps also the element that leads to the stop
    """
    for x in iterable:
        if predicate(x):
            yield x
        else:
            yield x
            break

def part1() -> int:
    # Part 1 of the puzzle
    trees = get_input()
    visible_tree_map = generate_visibility_map(trees)
    return(sum([row.count(1) for row in visible_tree_map]))
    

def part2() -> int:
    # Part 2 of the puzzle
    trees = get_input()
    trees_flat = [tree for row in trees for tree in row]
    scores = [get_view_score(trees_flat, idx, len(trees)) for idx in range(len(trees_flat))]
    return max(scores)

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")
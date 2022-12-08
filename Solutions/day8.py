from os import path
from typing import List, Tuple

# Set True for my inputs and False for test inputs
SOLUTION_MODE = False
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

def calculate_scenice_view(trees: List[List[int]], row_idx:int, col_idx: int):
    width, height = len(trees[0]), len(trees)
    tree = trees[row_idx][col_idx]
    visible_trees: List[int] = []
    # Check left if not on left border
    if col_idx > 0:
        first_tree = trees[row_idx][col_idx - 1]
        left_trees = 1
        for earlier_column in range(col_idx - 2, -1, -1):
            if earlier_column < 0:
                break
            if first_tree <= trees[row_idx][earlier_column]:
                left_trees += 1
                first_tree = trees[row_idx][earlier_column]
            if trees[row_idx][earlier_column] == 9 or earlier_column == 0 or tree < trees[row_idx][earlier_column]:
                break
        visible_trees.append(left_trees)
    else:
        visible_trees.append(0)

    # Check right if not on right border
    if col_idx < width - 1:
        first_tree = trees[row_idx][col_idx + 1]
        right_trees = 1
        for later_column in range(col_idx + 1, width):
            if first_tree <= trees[row_idx][later_column]:
                right_trees += 1
                first_tree = trees[row_idx][later_column]
            if trees[row_idx][later_column] == 9 or later_column == width - 1 or tree < trees[row_idx][later_column]:
                break
        visible_trees.append(right_trees)
    else:
        visible_trees.append(0)

    # Check up if not on upper border
    if row_idx > 0:
        first_tree = trees[row_idx - 1][col_idx]
        upper_trees = 1
        for earlier_row in range(row_idx - 2, -1, -1):
            if earlier_row < 0:
                break
            if first_tree <= trees[earlier_row][col_idx]:
                upper_trees += 1
                first_tree = trees[earlier_row][col_idx]
            if trees[earlier_row][col_idx] == 9 or earlier_row == 0 or tree < trees[earlier_row][col_idx]:
                break
        visible_trees.append(upper_trees)
    else:
        visible_trees.append(0)

    # Check down if not on lower border
    if row_idx < height - 1:
        first_tree = trees[row_idx + 1][col_idx]
        lower_trees = 1
        for later_row in range(row_idx + 1, height):
            if first_tree <= trees[later_row][col_idx]:
                lower_trees += 1
                first_tree = trees[later_row][col_idx]
            if trees[later_row][col_idx] == 9 or later_row == height - 1 or tree < trees[later_row][col_idx]:
                break
        visible_trees.append(lower_trees)
    else:
        visible_trees.append(0)

    product = 1
    for i in visible_trees:
        product *= i
    return(product, visible_trees)

def part1() -> int:
    # Part 1 of the puzzle
    pass
    # trees = get_input()
    # visible_tree_map = generate_visibility_map(trees)
    # return(sum([row.count(1) for row in visible_tree_map]))
    

def part2() -> int:
    # Part 2 of the puzzle
    trees = get_input()
    visible_trees = calculate_scenice_view(trees, 1, 2)
    print(visible_trees)

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")
from __future__ import annotations
from os import path
from typing import Dict, List


# Set True for my inputs and False for test inputs
SOLUTION_MODE = True
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

# create Classes for directories and files
class Directory():
    def __init__(self, name: str, parent_dir: Directory) -> None:
        self.name = name
        self.parent_dir: Directory = parent_dir
        self._subdirectories: Dict[str, Directory] = {}
        self._files: Dict[str, File] = {}
        self._size = 0

    def calculate_size(self) -> int:
        """
        Calculates size of the directory by adding up file and subdirectory sizes
        Subdirectory sizes are calculated recursively
        """
        for subdir in self._subdirectories.values():
            subdir.calculate_size()
            self._size += subdir.get_size()
        for file in self._files.values():
            self._size += file.get_size()

    def get_size(self) -> int:
        """
        Return the size of the directory
        """
        return self._size

    def add_directory(self, subdir: Directory) -> None:
        """
        Adds a new subdirectory to the dictionary of subdirectories
        """
        self._subdirectories[subdir.name] = subdir

    def add_file(self, file: File) -> None:
        """
        Adds a new file to the dictionary of files
        """
        self._files[file.name] = file

    def go_to_parent(self) -> Directory:
        """
        Returns the parent directory, e.g. moves up one directory
        """
        return self.parent_dir

    def move_to_subdir(self, subdir_name: str) -> Directory:
        """
        Returns the subdirectory according to a name, e.g. moves down one directory
        """
        if subdir_name in self._subdirectories:
            return self._subdirectories[subdir_name]
        else:
            return None

class File():
    def __init__(self, name: str, size:int) -> None:
        self.name: str = name
        self._size:int = int(size)

    def get_size(self) -> int:
        """
        Return the size of the file
        """
        return self._size

# Open and prepare input
def get_input() -> List[str]:
    with open(path.join(data_folder, "day7.txt"), "r") as file:
        content = file.read()
        return content.split("\n")[2:] # Do not return the first two lines: $ cd / and $ ls as they just go to the base dir and then list the content

def walk_through_inputs(input: List[str]):
    # Create base directory and set it as active
    basedir = Directory(name = "/", parent_dir=None)
    current_dir = basedir

    # Walk through each input
    for line in input:
        # print(f"Current dir is: {current_dir.name}")

        # Add new directory to current directory; line will be in format 'dir xyz', so splitting by ' ' will yield the dirname as second item
        if line.startswith("dir"):
            dirname = line.split(" ")[1]
            new_dir = Directory(name = dirname, parent_dir = current_dir)
            current_dir.add_directory(new_dir)
            # print(f"Added new directory to {current_dir.name} named {new_dir.name}")

        # Do nothing if ls command is thrown, as there are no new information
        elif line.startswith("$ ls"):
            continue

        # Move to the directory as specified, will be either .. or directory name
        elif line.startswith("$ cd"):
            if ".." in line:
                current_dir = current_dir.go_to_parent()
            else:
                subdir_name = line.split("cd ")[1]
                current_dir = current_dir.move_to_subdir(subdir_name=subdir_name)

        # Add new file to directory; format will be '123456 filename' so splitting by ' ' will yield the size and filename
        else:
            file_size, file_name = line.split(" ")
            new_file = File(name = file_name, size = file_size)
            current_dir.add_file(new_file)
    
    # Calculate size recursively
    basedir.calculate_size()

    return basedir

def get_size_directories_under100k(basedir: Directory) -> int:
    output:int = 0
    for subdir in basedir._subdirectories.values():
        if subdir.get_size() <= 100000:
            output += subdir.get_size()
        
        # Recursively go through all subdirectories and add to the total if under 100001 in size
        output += get_size_directories_under100k(subdir)
    return output

def get_sizes_over_needed_space(basedir: Directory, needed_space: int) -> List[int]:
    output: List[int] = []
    for subdir in basedir._subdirectories.values():
        if subdir.get_size() >= needed_space:
            output.append(subdir.get_size())
        
        # Recursively go through all subdirectories and the size if bigger than the required space
        output.extend(get_sizes_over_needed_space(subdir, needed_space))
    return output

def part1() -> int:
    # Part 1 of the puzzle
    lines = get_input()
    basedir = walk_through_inputs(lines)
    return get_size_directories_under100k(basedir=basedir)
    
def part2() -> int:
    # Part 2 of the puzzle
    lines = get_input()
    basedir = walk_through_inputs(lines)

    # Calculate the amount of space that needs to be freed as a minimum
    unused_space = 70000000 - basedir.get_size()
    needed_space = 30000000 - unused_space

    # Get all directories that are bigger than the required size, sort them and take the smallest
    possible_directories = sorted(get_sizes_over_needed_space(basedir=basedir, needed_space=needed_space))
    return possible_directories[0]

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}")
    print(f"Solution to Part2: {part2()}")
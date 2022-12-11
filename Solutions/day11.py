from os import path
from typing import List, Tuple
from queue import SimpleQueue

# Set True for my inputs and False for test inputs
SOLUTION_MODE = False
data_folder = "Inputs" if SOLUTION_MODE else "Test_inputs"

class Monkey():
    def __init__(self, monkey_number:int, items:str, increase_operation:str, test:int, throw_true:int, throw_false:int) -> None:
        self.monkey_number = monkey_number
        self.items: SimpleQueue = self.create_queue(items)
        self.operator, self.increase = self.parse_increase_operation(increase_operation)
        self.test:int = test
        self.throw_true:int = throw_true
        self.throw_false:int = throw_false
        self.inspected_items:int = 0

    def parse_increase_operation(self, increase_operation:str) -> Tuple[int]:
        """
        Operations can be '* x', '+ x' or '* old'. Function creates the operation mode and the number to operate with
        operator is 'decoded' in the throw_item function
        """
        operator:int = 0 if increase_operation[0] == "*" else 1
        increase:int|str = increase_operation.split(" ")[1]
        if increase == "old":
            operator = 2
            increase:int = 0
        else:
            increase:int = int(increase)

        return (operator, increase)

    def create_queue(self, items:str) -> SimpleQueue:
        """
        Create FIFO-Queue of items
        Input is a string with the format 'Starting items: x, y, z' so item worry levels start at position 17
        """
        item_queue = SimpleQueue()
        for i in items[17:].split(", "):
            item_queue.put_nowait(Item(int(i)))
        return item_queue

    def throw_item_part1(self) -> Tuple:
        """
        Inspects and throws the next item in the queue
        worry is calculated according to increase operation, then divided by 3 as monkey loses interest
        After calculating the worry level, the inspected item level is incremented
        Returns: Tuple[int, Item], contains the monkey to throw the item to and the current item
        """
        if self.items.empty():
            return tuple(-1)

        current_item:Item = self.items.get_nowait()

        if self.operator == 0:
            current_item.current_worry = (current_item.current_worry * self.increase) // 3
        elif self.operator == 1:
            current_item.current_worry = (current_item.current_worry + self.increase) // 3
        elif self.operator == 2:
            current_item.current_worry = (current_item.current_worry * current_item.current_worry) // 3
            
        self.inspected_items += 1

        return (self.throw_true, current_item) if current_item.current_worry % self.test == 0 else (self.throw_false, current_item)

    def throw_item_part2(self) -> Tuple:
        """
        Inspects and throws the next item in the queue
        worry is calculated according to increase operation, but only remainders are used for calculation
        After calculating the worry level, the inspected item level is incremented
        Returns: Tuple[int, Item], contains the monkey to throw the item to and the current item
        """
        if self.items.empty():
            return tuple(-1)

        current_item:Item = self.items.get_nowait()
        current_item.update_worry(self.increase, self.operator)

        self.inspected_items += 1

        return (self.throw_true, current_item) if current_item.worry[self.monkey_number] == 0 else (self.throw_false, current_item)

    def get_inspected_items(self) -> int:
        """
        Returns the number of inspected items
        """
        return self.inspected_items

class Item():
    def __init__(self, worry:int):
        self.initial_worry = worry
        self.current_worry = worry
        self.monkey_divider = [11,7,3,5,17,13,19,2]
        self.worry:List[int] = self.initialize_worry(worry)

    def __repr__(self) -> str:
        return ", ".join([str(i) for i in self.worry])

    def initialize_worry(self, worry:int) -> List[int]:
        """
        Generates the list of initial remainders for each monkey; monkey_divider are prewritten, could be extracted from text
        """
        return [worry % monkey_divider for monkey_divider in self.monkey_divider]

    def update_worry(self, increase:int, operator:int) -> None:
        """
        Update the worry-list by remainder math
        """
        if operator == 0:
            self.worry = [(worry * increase) % self.monkey_divider[idx] if worry > 0 else worry for idx, worry in enumerate(self.worry)]
        elif operator == 1:
            self.worry = [(worry + increase) % self.monkey_divider[idx] for idx, worry in enumerate(self.worry)]
        elif operator == 2:
            self.worry = [(worry * worry) % self.monkey_divider[idx] if worry > 0 else worry for idx, worry in enumerate(self.worry)]
    

# Open and prepare input
def get_input() -> List[Monkey]:
    with open(path.join(data_folder, "day11.txt"), "r") as file:
        monkey_descriptions:List[str] = file.read().split("\n\n")
        monkeys:List[Monkey] = []
        for monkey_number, monkey in enumerate(monkey_descriptions):
            lines: List[str] = monkey.splitlines()
            increase_operation:str = lines[2].split("new = old ")[1]
            test:int = int(lines[3].split(" by ")[1])
            throw_true:int = int(lines[4][-1])
            throw_false:int = int(lines[5][-1])
            new_monkey:Monkey = Monkey(monkey_number, lines[1], increase_operation, test, throw_true, throw_false)
            monkeys.append(new_monkey)
        return monkeys


def part1() -> int:
    # Part 1 of the puzzle
    monkeys = get_input()
    for _ in range(20):
        for monkey in monkeys:
            while monkey.items.qsize() > 0:
                new_monkey, item = monkey.throw_item_part1()
                monkeys[new_monkey].items.put_nowait(item)
    inspections = sorted([monkey.get_inspected_items() for monkey in monkeys])
    return inspections[-1] * inspections[-2]
    

def part2() -> int:
    # Part 2 of the puzzle
    monkeys = get_input()
    for i in range(10000):
        for monkey in monkeys:
            while monkey.items.qsize() > 0:
                new_monkey, item = monkey.throw_item_part2()
                monkeys[new_monkey].items.put_nowait(item)
    inspections = sorted([monkey.get_inspected_items() for monkey in monkeys])
    return inspections[-1] * inspections[-2]

if __name__ == "__main__":
    print(f"Solution to Part1: {part1()}") # 102399
    print(f"Solution to Part2: {part2()}") # 23641658401
# Open input, split by empty new line; then sum all calories for each elf
with open("input1.txt", "r") as file:
    content = file.read()
    elf_food = content.split("\n\n")
    elf_calories = [sum([int(calory) for calory in elf.split("\n")]) for elf in elf_food]

# Answer 1
print(max(elf_calories))

# Answer 2 (sort the calories by amount and only get the top 3, then sum them up)
elf_calories.sort()
print(sum(elf_calories[-3:]))
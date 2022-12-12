"""
--- Day 5: Supply Stacks ---

The expedition can depart as soon as the final supplies have been unloaded from the ships. Supplies are stored in stacks of marked crates, but because the needed supplies are buried under many other crates, the crates need to be rearranged.

The ship has a giant cargo crane capable of moving crates between stacks. To ensure none of the crates get crushed or fall over, the crane operator will rearrange them in a series of carefully-planned steps. After the crates are rearranged, the desired crates will be at the top of each stack.

The Elves don't want to interrupt the crane operator during this delicate procedure, but they forgot to ask her which crate will end up where, and they want to be ready to unload them as soon as possible so they can embark.

They do, however, have a drawing of the starting stacks of crates and the rearrangement procedure (your puzzle input). For example:

    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2

In this example, there are three stacks of crates. Stack 1 contains two crates: crate Z is on the bottom, and crate N is on top. Stack 2 contains three crates; from bottom to top, they are crates M, C, and D. Finally, stack 3 contains a single crate, P.

Then, the rearrangement procedure is given. In each step of the procedure, a quantity of crates is moved from one stack to a different stack. In the first step of the above rearrangement procedure, one crate is moved from stack 2 to stack 1, resulting in this configuration:

[D]        
[N] [C]    
[Z] [M] [P]
 1   2   3 

In the second step, three crates are moved from stack 1 to stack 3. Crates are moved one at a time, so the first crate to be moved (D) ends up below the second and third crates:

        [Z]
        [N]
    [C] [D]
    [M] [P]
 1   2   3

Then, both crates are moved from stack 2 to stack 1. Again, because crates are moved one at a time, crate C ends up below crate M:

        [Z]
        [N]
[M]     [D]
[C]     [P]
 1   2   3

Finally, one crate is moved from stack 1 to stack 2:

        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   3

The Elves just need to know which crate will end up on top of each stack; in this example, the top crates are C in stack 1, M in stack 2, and Z in stack 3, so you should combine these together and give the Elves the message CMZ.

After the rearrangement procedure completes, what crate ends up on top of each stack?
"""


def get_stacks(lines: list[str]) -> tuple[int, list[list[str]]]:
    num_stacks = 0
    height = -1
    for index, line in enumerate(lines):
        if line[0] == " " and line[1] != "[" and line[1] != " ":  # stack numbers
            num_stacks = int(line[-2])
            height = index
            break
    stacks = [[] for _ in range(num_stacks)]
    for line in range(height - 1, -1, -1):
        for stack_index in range(num_stacks):
            value = lines[line][stack_index * 4 + 1]
            if value != " ":
                stacks[stack_index].append(value)
    return (height, stacks)


def simulate_move(stacks: list[list[str]], move: str) -> list[list[str]]:
    split_move_string = move.split(" ")
    num_crates = int(split_move_string[1])
    from_stack = int(split_move_string[3]) - 1
    to_stack = int(split_move_string[5]) - 1
    for _ in range(num_crates):
        stacks[to_stack].append(stacks[from_stack].pop())
    return stacks


def part_one(lines: list[str]) -> str:
    height, stacks = get_stacks(lines)
    for move in lines[height + 1 :]:
        if move == "":
            continue
        stacks = simulate_move(stacks, move)
    return "".join([stack[-1] for stack in stacks])


"""
--- Part Two ---

As you watch the crane operator expertly rearrange the crates, you notice the process isn't following your prediction.

Some mud was covering the writing on the side of the crane, and you quickly wipe it away. The crane isn't a CrateMover 9000 - it's a CrateMover 9001.

The CrateMover 9001 is notable for many new and exciting features: air conditioning, leather seats, an extra cup holder, and the ability to pick up and move multiple crates at once.

Again considering the example above, the crates begin in the same configuration:

    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

Moving a single crate from stack 2 to stack 1 behaves the same as before:

[D]        
[N] [C]    
[Z] [M] [P]
 1   2   3 

However, the action of moving three crates from stack 1 to stack 3 means that those three moved crates stay in the same order, resulting in this new configuration:

        [D]
        [N]
    [C] [Z]
    [M] [P]
 1   2   3

Next, as both crates are moved from stack 2 to stack 1, they retain their order as well:

        [D]
        [N]
[C]     [Z]
[M]     [P]
 1   2   3

Finally, a single crate is still moved from stack 1 to stack 2, but now it's crate C that gets moved:

        [D]
        [N]
        [Z]
[M] [C] [P]
 1   2   3

In this example, the CrateMover 9001 has put the crates in a totally different order: MCD.

Before the rearrangement process finishes, update your simulation so that the Elves know where they should stand to be ready to unload the final supplies. After the rearrangement procedure completes, what crate ends up on top of each stack?
"""


def simulate_move_with_order(stacks: list[list[str]], move: str) -> list[list[str]]:
    split_move_string = move.split(" ")
    num_crates = int(split_move_string[1])
    from_stack = int(split_move_string[3]) - 1
    to_stack = int(split_move_string[5]) - 1
    stacks[to_stack].extend(stacks[from_stack][-num_crates:])
    stacks[from_stack] = stacks[from_stack][:-num_crates]
    return stacks


def part_two(lines: list[str]) -> str:
    height, stacks = get_stacks(lines)
    for move in lines[height + 1 :]:
        if move == "":
            continue
        stacks = simulate_move_with_order(stacks, move)
    return "".join([stack[-1] for stack in stacks])


def main():
    with open("example.txt") as f:
        lines = f.read().splitlines()
    print(part_one(lines))
    print(part_two(lines))

    with open("input.txt") as f:
        lines = f.read().splitlines()
    print(part_one(lines))
    print(part_two(lines))


if __name__ == "__main__":
    main()

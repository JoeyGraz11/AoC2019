from typing import List, Tuple
# Op Codes
# 1 -> addition (3 parameters)
# 2 -> multiplication (3 parameters)
# 3 -> read from input store at address (1 parameter)
# 4 -> read from address and output (1 parameter)
# 5 -> jump-if-true (2 parameters)
# 6 -> jump-if-false (2 parameters)
# 7 -> test: first less than second store at third (3 parameters)
# 8 -> test: first equals second store at third (3 parameters)
# 9 -> increment relative base by value of parameter (1 parameter)
# 99 -> STOP

NUM_PARAM = {1: 3, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 9: 1, 99: 0}


def parse_instruction(inst: int) -> Tuple[int, List[int]]:
    inst = str(inst)
    opcode = int(inst[-2:])
    modes = [int(i) for i in inst[:-2]]
    for i in range(NUM_PARAM[opcode] - len(modes)):
        modes.insert(0, 0)

    return opcode, modes


def get_param(data: List[int], index: int, mode: int, rel_base: int) -> int:
    value = data[index]
    if mode == 0:
        return data[value]
    elif mode == 1:
        return value
    elif mode == 2:
        return data[value + rel_base]
    else:
        raise TypeError('Bad mode!')


def computer(data: List[int], pointer: int = 0, start_value: List[int] = (0, 0), relative_base: int = 0):
    output = []

    while len(output) < 1:
        increment_pointer = True
        instruction = data[pointer]

        opcode, modes = parse_instruction(instruction)

        # Sets the write location
        if modes and modes[0] == 2:
            access_loc = data[pointer + NUM_PARAM[opcode]] + relative_base
        else:
            access_loc = data[pointer + NUM_PARAM[opcode]]

        # Add
        if opcode == 1:
            data[access_loc] = get_param(data, pointer + 1, modes[-1], relative_base) + get_param(data, pointer + 2, modes[-2], relative_base)
        # Multiply
        elif opcode == 2:
            data[access_loc] = get_param(data, pointer + 1, modes[-1], relative_base) * get_param(data, pointer + 2, modes[-2], relative_base)
        # Read and store input
        elif opcode == 3:
            if start_value:
                data[access_loc] = start_value.pop(0)  # Writing input may change
        # Write output
        elif opcode == 4:
            #print(get_param(data, pointer + 1, modes[-1], relative_base))
            output.append(get_param(data, pointer + 1, modes[-1], relative_base))
        # Jump if not 0
        elif opcode == 5:
            if get_param(data, pointer + 1, modes[-1], relative_base) != 0:
                pointer = get_param(data, pointer + 2, modes[-2], relative_base)
                increment_pointer = False
        # Jump if 0
        elif opcode == 6:
            if get_param(data, pointer + 1, modes[-1], relative_base) == 0:
                pointer = get_param(data, pointer + 2, modes[-2], relative_base)
                increment_pointer = False
        # True if less than
        elif opcode == 7:
            if get_param(data, pointer + 1, modes[-1], relative_base) < get_param(data, pointer + 2, modes[-2], relative_base):
                data[access_loc] = 1
            else:
                data[access_loc] = 0
        # True if equal to
        elif opcode == 8:
            if get_param(data, pointer + 1, modes[-1], relative_base) == get_param(data, pointer + 2, modes[-2], relative_base):
                data[access_loc] = 1
            else:
                data[access_loc] = 0
        # Increment relative base
        elif opcode == 9:
            relative_base += get_param(data, pointer + 1, modes[-1], relative_base)
        # End
        elif opcode == 99:
            return False

        else:
            raise ValueError('Bad opcode')

        if increment_pointer:
            pointer += NUM_PARAM[opcode] + 1

    if len(output) == 1:
        output = output[0]

    return data, pointer, start_value, relative_base, output

# ---- Day 15: Part 1 ----

def draw_maze(maze, cur_pos):
    convert = {0: '█', 1: '.', 2: '!', 3: 'o'}
    min_x = min([i[0] for i in maze])
    max_x = max([i[0] for i in maze])
    min_y = min([i[1] for i in maze])
    max_y = max([i[1] for i in maze])

    y_list = [i for i in range(min_y, max_y + 1)]

    print('---------------------------------')
    for y in y_list[::-1]:
        row = []
        for x in range(min_x, max_x + 1):
            if (x, y) in maze:
                if (x, y) == cur_pos:
                    row.append('D')
                elif (x, y) == (0, 0):
                    row.append('*')
                else:
                    row.append(convert[maze[x, y]])
            else:
                row.append(' ')
        print(''.join(row))


with open('input.txt', 'r') as file:
    data = [int(i) for i in file.read().split(',')]
    data.extend([0] * len(data) * 10)


# 1: north
# 2: south
# 3: west
# 4: east
take_step = {
    1: lambda coord: (coord[0], coord[1] + 1),
    2: lambda coord: (coord[0], coord[1] - 1),
    3: lambda coord: (coord[0] - 1, coord[1]),
    4: lambda coord: (coord[0] + 1, coord[1]),
}

forward = {
    'north': 1,
    'south': 2,
    'west': 3,
    'east': 4
}
right = {
    'north': 'east',
    'south': 'west',
    'east': 'south',
    'west': 'north'
}
left = {
    'north': 'west',
    'south': 'east',
    'east': 'north',
    'west': 'south'
}


checked_right = False
facing = 'east'
cur_pos = (0, 0)
explored = {cur_pos: 1}  # (x, y): int
input = 4
output = computer(data, pointer=0, start_value=[input], relative_base=0)

i = 0
while True:
    explored[take_step[input](cur_pos)] = output[4]

    if output[4] != 0:
        cur_pos = take_step[input](cur_pos)

    if cur_pos == (0, 0) and i > 5:
        break

    if output[4] == 0:
        facing = left[facing]
        input = forward[facing]
    else:
        facing = right[facing]
        input = forward[facing]

    output = computer(data, pointer=0, start_value=[input], relative_base=0)
    i += 1

draw_maze(explored, cur_pos)

# ---- Part 2 ----
branches = [i for i in explored if explored[i] == 2]  # Should only be 1 (x, y) location here
branches[0] = (branches[0], 0)  # [((x, y), time)]
max_time = 0

while branches:
    current = branches.pop(0)
    loc = current[0]
    time = current[1]

    to_check = [take_step[i](loc) for i in range(1, 5)]

    for coord in to_check:
        if coord in explored and explored[coord] != 0 and explored[coord] != 3:
            explored[coord] = 3
            branches.append((coord, time + 1))

            if time + 1 > max_time:
                max_time = time + 1


draw_maze(explored, cur_pos)
print(max_time)
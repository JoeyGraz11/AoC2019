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

    while len(output) < 2:
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

    return data, pointer, start_value, relative_base, output



# ---- Day 11 Part 1----

def draw_panels(panels):
    convert = {0: ' ', 1: '█'}
    min_x = min([i[0] for i in panels])
    max_x = max([i[0] for i in panels])
    min_y = min([i[1] for i in panels])
    max_y = max([i[1] for i in panels])

    y_list = [i for i in range(min_y, max_y + 1)]

    for y in y_list[::-1]:
        row = []
        for x in range(min_x, max_x + 1):
            if (x, y) in panels:
                row.append(convert[panels[x, y]])
            else:
                row.append(convert[0])
        print(''.join(row))


with open('input.txt', 'r') as file:
    data = [int(i) for i in file.read().split(',')]
    data.extend([0] * len(data) * 10)

    next_move = {
        ('up', 0): 'left',
        ('up', 1): 'right',
        ('left', 0): 'down',
        ('left', 1): 'up',
        ('down', 0): 'right',
        ('down', 1): 'left',
        ('right', 0): 'up',
        ('right', 1): 'down'
    }

    take_step = {
        'left': lambda coord: (coord[0] - 1, coord[1]),
        'right': lambda coord: (coord[0] + 1, coord[1]),
        'up': lambda coord: (coord[0], coord[1] + 1),
        'down': lambda coord: (coord[0], coord[1] - 1),
    }

    heading = [(0, 0), 'up']
    panels = {}  # (x, y): 0 (black) or 1 (white)

    output = computer(data, pointer=0, start_value=[1], relative_base=0)
    while output:
        panels[heading[0]] = output[4][0]

        heading[1] = next_move[heading[1], output[4][1]]  # New direction
        heading[0] = take_step[heading[1]](heading[0])  # Move in that direction

        if heading[0] in panels:
            color_under = panels[heading[0]]
        else:
            color_under = 0

        output = computer(output[0], pointer=output[1], start_value=[color_under], relative_base=output[3])

    print(len(panels))

    draw_panels(panels)
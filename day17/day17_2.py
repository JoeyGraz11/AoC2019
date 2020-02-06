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


def computer(data: List[int], input = None):
    pointer = 0
    relative_base = 0

    output = []

    while True:
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
            if input:
                data[access_loc] = input.pop(0)
            else:
                print('Need input!')
                return
        # Write output
        elif opcode == 4:
            yield get_param(data, pointer + 1, modes[-1], relative_base)
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
            return

        else:
            raise ValueError('Bad opcode')

        if increment_pointer:
            pointer += NUM_PARAM[opcode] + 1




def draw_map(maze):
    convert = {35: '#', 46: '.', 10: '', 60: '<', 62: '>', 79: 'O', 94: '^', 118: 'v', 86: 'v'}
    min_x = min([i[0] for i in maze])
    max_x = max([i[0] for i in maze])
    min_y = min([i[1] for i in maze])
    max_y = max([i[1] for i in maze])

    y_list = [i for i in range(min_y, max_y + 1)]

    print('\n+----------------------------------------------------------+\n')
    for y in y_list[::-1]:
        row = []
        for x in range(min_x, max_x + 1):
            if (x, y) in maze:
                row.append(convert[maze[x, y]])
        print(''.join(row))

# ---- Day 17: Part 1 ----
with open('input.txt', 'r') as file:
    data = [int(i) for i in file.read().split(',')]
    data.extend([0] * len(data) * 10)

view = {}  # (x, y)

x = 0
y = 0
for out in computer(data):
    print(out)
    view[(x, y)] = out
    if out != 10:
        x += 1
    else:
        y += 1
        x = -1

draw_map(view)

def check_neighbor(coord):
    take_step = {
        1: lambda coord: (coord[0], coord[1] + 1),
        2: lambda coord: (coord[0], coord[1] - 1),
        3: lambda coord: (coord[0] - 1, coord[1]),
        4: lambda coord: (coord[0] + 1, coord[1]),
    }
    res = True
    neighbors = [take_step[i](coord) for i in range(1, 5)]
    for n in neighbors:
        if n not in view:
            continue
        res = res and view[n] == 35
    return res


scaffold = [coord for coord, val in view.items() if val == 35]
intersection = []

for coord in scaffold:
    if check_neighbor(coord):
        view[coord] = 79
        intersection.append(coord)

print(sum([i*j for i, j in intersection]))

# ---- Day 17: Part 2 ----
with open('input.txt', 'r') as file:
    data = [int(i) for i in file.read().split(',')]
    data.extend([0] * len(data) * 15)
    data[0] = 2

ascii = {'R': 82, 'L': 76, ',': 44, 'A': 65, 'B': 66, 'C': 67, '4': 52, '6': 54, '8': 56, '/': 10, 'n': 110}

func_A = [ascii[i] for i in 'R,6,6,R,8,R,8,L,4,R,6,6,R,6,6,L,6/']
func_B = [ascii[i] for i in 'R,6,6,L,4,R,6,6,L,6/']
func_C = [ascii[i] for i in 'L,6,6,R,8,R,8/']
func_main = [ascii[i] for i in 'C,B,A,B,A,A,B/']
func_draw = [ascii[i] for i in 'n/']
all_func = [func_main, func_A, func_B, func_C, func_draw]

output = computer(data, func_main)

for func in all_func:
    for out in enumerate(computer(data, input=func)):
        print(out)


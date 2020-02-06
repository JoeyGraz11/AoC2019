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
# 99 -> STOP

NUM_PARAM = {1: 3, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 99: 0}


def parse_instruction(inst: int) -> Tuple[int, List[int]]:
    inst = str(inst)
    opcode = int(inst[-2:])
    modes = [int(i) for i in inst[:-2]]
    for i in range(NUM_PARAM[opcode] - len(modes)):
        modes.insert(0, 0)

    return opcode, modes


def get_param(data: List[int], index: int, mode: int) -> int:
    value = data[index]
    if mode == 0:
        return data[value]
    elif mode == 1:
        return value
    else:
        raise TypeError('Bad mode!')


def computer(data: List[int], pointer: int = 0, start_value: List[int] = (0, 0)) -> Tuple[int, bool, int]:
    increment_pointer = True
    instruction = data[pointer]

    opcode, modes = parse_instruction(instruction)

    access_loc = data[pointer + NUM_PARAM[opcode]]
    if opcode == 1:
        data[access_loc] = get_param(data, pointer + 1, modes[-1]) + get_param(data, pointer + 2, modes[-2])

    elif opcode == 2:
        data[access_loc] = get_param(data, pointer + 1, modes[-1]) * get_param(data, pointer + 2, modes[-2])

    elif opcode == 3:
        data[access_loc] = start_value.pop(0)  # Writing input may change

    elif opcode == 4:
        return get_param(data, pointer + 1, modes[-1]), False, pointer + 2

    elif opcode == 5:
        if get_param(data, pointer + 1, modes[-1]) != 0:
            pointer = get_param(data, pointer + 2, modes[-2])
            increment_pointer = False

    elif opcode == 6:
        if get_param(data, pointer + 1, modes[-1]) == 0:
            pointer = get_param(data, pointer + 2, modes[-2])
            increment_pointer = False

    elif opcode == 7:
        if get_param(data, pointer + 1, modes[-1]) < get_param(data, pointer + 2, modes[-2]):
            data[access_loc] = 1
        else:
            data[access_loc] = 0

    elif opcode == 8:
        if get_param(data, pointer + 1, modes[-1]) == get_param(data, pointer + 2, modes[-2]):
            data[access_loc] = 1
        else:
            data[access_loc] = 0

    elif opcode == 99:
        return None, True, pointer  # get_param(data, pointer + 1, modes[-1]), True, pointer
    else:
        raise ValueError('Bad opcode')

    if increment_pointer:
        pointer += NUM_PARAM[opcode] + 1

    out = computer(data, pointer, start_value=start_value)
    if out:
        return out



# --- Day 7 ---
from itertools import permutations

with open('input.txt', 'r') as file:
    data = [int(i) for i in file.read().split(',')]

    max = 0
    for perm in permutations((5, 6, 7, 8, 9)):
        data_a = data.copy()
        data_b = data.copy()
        data_c = data.copy()
        data_d = data.copy()
        data_e = data.copy()

        a = computer(data_a, start_value=[perm[0], 0])
        i = 0
        e = (0, False, 0)
        while not e[1]:
            if i != 0:
                a = computer(data_a, start_value=[e[0]], pointer=a[2])
                b = computer(data_b, start_value=[a[0]], pointer=b[2])
                c = computer(data_c, start_value=[b[0]], pointer=c[2])
                d = computer(data_d, start_value=[c[0]], pointer=d[2])
                e = computer(data_e, start_value=[d[0]], pointer=e[2])
                if e[0] and e[0] > max:
                    max = e[0]
            else:
                b = computer(data_b, start_value=[perm[1], a[0]])
                c = computer(data_c, start_value=[perm[2], b[0]])
                d = computer(data_d, start_value=[perm[3], c[0]])
                e = computer(data_e, start_value=[perm[4], d[0]])

            i += 1

    print(max)
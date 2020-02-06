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


def computer(data: List[int], pointer: int = 0, start_value: int = 1) -> None:
    increment_pointer = True
    instruction = data[pointer]

    opcode, modes = parse_instruction(instruction)

    access_loc = data[pointer + NUM_PARAM[opcode]]
    if opcode == 1:
        data[access_loc] = get_param(data, pointer + 1, modes[-1]) + get_param(data, pointer + 2, modes[-2])

    elif opcode == 2:
        data[access_loc] = get_param(data, pointer + 1, modes[-1]) * get_param(data, pointer + 2, modes[-2])

    elif opcode == 3:
        data[access_loc] = start_value  # Writing input may change

    elif opcode == 4:
        print(get_param(data, pointer + 1, modes[-1]))  # Write data may change

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
        return
    else:
        raise ValueError('Bad opcode')

    if increment_pointer:
        pointer += NUM_PARAM[opcode] + 1

    computer(data, pointer)


with open('input.txt', 'r') as file:
    data = [int(i) for i in file.read().split(',')]
    computer(data, start_value=5)

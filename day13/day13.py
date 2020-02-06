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

    while len(output) < 3:
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

# ---- Day 13: Part 1 ----
with open('input.txt', 'r') as file:
    data = [int(i) for i in file.read().split(',')]
    data.extend([0] * len(data) * 10)

    block_count = 0
    output = computer(data, pointer=0, start_value=[], relative_base=0)
    while output:
        if output[4][2] == 2:
            block_count += 1
        output = computer(output[0], pointer=output[1], start_value=[], relative_base=output[3])

print(f'{block_count} total blocks')

# ---- Day 13: Part 2 ----
with open('input.txt', 'r') as file:
    data = [int(i) for i in file.read().split(',')]
    data[0] = 2
    data.extend([0] * len(data) * 10)

    score = 0
    paddle_pos = [0, 0]
    output = computer(data, pointer=0, start_value=[], relative_base=0)
    while output:
        if output[4][2] == 3:  # This is paddle position
            paddle_pos[0] = output[4][0]
            paddle_pos[1] = output[4][1]

        if output[4][2] == 4:  # This is the ball's loc
            if output[4][0] > paddle_pos[0]:
                input = 1
            elif output[4][0] < paddle_pos[0]:
                input = -1
            else:
                input = 0

        if output[4][0] == -1 and output[4][1] == 0:
            score = output[4][2]

        output = computer(output[0], pointer=output[1], start_value=[input], relative_base=output[3])

print(score)
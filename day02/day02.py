def operate(line, data):
    opcode = line[0]
    loc1 = line[1]
    loc2 = line[2]
    loc_res = line[3]

    if opcode == 1:
        data[loc_res] = data[loc1] + data[loc2]
        return True
    elif opcode == 2:
        data[loc_res] = data[loc1] * data[loc2]
        return True
    elif opcode == 99:
        return False


def computer(data):
        lines = []
        line = []
        for i, op in enumerate(data):
            if i % 4 == 0 and i != 0:
                lines.append(line)
                line = []
            line.append(op)

        for line in lines:
            if not operate(line, data):
                break

        return data[0]


with open('input.txt', 'r') as file:
    clean_data = [int(i) for i in file.read().split(',')]
    for i in range(0, 100):
        for j in range(0, 100):
            data = clean_data.copy()
            data[1] = i
            data[2] = j
            if computer(data) == 19690720:
                print(100 * i + j)
                break

from itertools import tee

def pairwise(iterable):
    # s -> (s0,s1), (s1,s2), (s2, s3), ...
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def load_input(file):
    with open(file, 'r') as f:
        w1 = [i.strip() for i in f.readline().split(',')]
        w2 = [i.strip() for i in f.readline().split(',')]
    return w1, w2


def make_wire(wire_input):
    wire = [(0, 0)]
    for i in wire_input:
        val = int(i[1:])
        if i[0] == 'R':
            wire.append((wire[-1][0] + val, wire[-1][1]))
        elif i[0] == 'L':
            wire.append((wire[-1][0] - val, wire[-1][1]))
        elif i[0] == 'U':
            wire.append((wire[-1][0], wire[-1][1] + val))
        elif i[0] == 'D':
            wire.append((wire[-1][0], wire[-1][1] - val))
    return wire


def intersect(line1, line2):
    x1 = line1[0][0]
    x2 = line1[1][0]
    x3 = line2[0][0]
    x4 = line2[1][0]
    y1 = line1[0][1]
    y2 = line1[1][1]
    y3 = line2[0][1]
    y4 = line2[1][1]

    bot = (x4 - x3)*(y1 - y2) - (x1 - x2)*(y4 - y3)
    if bot == 0:
        return None
    top_a = (y3 - y4)*(x1 - x3) + (x4 - x3)*(y1 - y3)
    top_b = (y1 - y2)*(x1 - x3) + (x2 - x1)*(y1 - y3)

    ta = top_a/bot
    tb = top_b/bot

    if 0 <= ta <= 1 and 0 <= tb <= 1:
        return x1 + ta*(x2 - x1), y1 + ta*(y2 - y1), abs(x1 + ta*(x2 - x1)) + abs(y1 + ta*(y2 - y1))
    else:
        return None


w1, w2 = load_input('input.txt')
wire1 = make_wire(w1)
wire2 = make_wire(w2)

lines1 = [i for i in pairwise(wire1)]
lines2 = [i for i in pairwise(wire2)]

# Part 1
distances = []
for line1 in lines1:
    for line2 in lines2:
        val = intersect(line1, line2)
        if val and val[2] != 0:
            distances.append(val[2])

print(min(distances))

# Part 2
distances = []
steps1 = 0
for line1 in lines1:
    steps1 += abs(line1[0][0] - line1[1][0]) + abs(line1[0][1] - line1[1][1])

    steps2 = 0
    for line2 in lines2:
        steps2 += abs(line2[0][0] - line2[1][0]) + abs(line2[0][1] - line2[1][1])

        val = intersect(line1, line2)
        if val and val[2] != 0:
            if line1[0][0] == line1[1][0]:  # 1st line is vertical
                f1 = steps1 - abs(line1[1][1] - val[1])
                f2 = steps2 - abs(line2[1][0] - val[0])
            else:  # 1st line is horizontal
                f1 = steps1 - abs(line1[1][0] - val[0])
                f2 = steps2 - abs(line2[1][1] - val[1])

            distances.append(f1 + f2)

print(min(distances))





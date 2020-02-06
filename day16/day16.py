from typing import List
from math import ceil

# ---- Day 16: Part 1 ----
BASE_PATTERN = [0, 1, 0, -1]

input = None
with open('input.txt', 'r') as file:
    input = file.readline()
    input = [int(i) for i in input]

def make_pattern(repetitions: int, length: int) -> List[int]:
    pattern = []
    for i in BASE_PATTERN:
        pattern.extend([i for _ in range(repetitions)])
    num_repeat = ceil(length / len(pattern))
    return_pattern = pattern[1:]
    for _ in range(num_repeat):
        return_pattern.extend(pattern)
    return_pattern = return_pattern[:length]
    return return_pattern


def get_ones(num: int) -> int:
    return abs(num) % 10


def run_phase(input):
    phase = []
    for ind, num in enumerate(input):
        pattern = make_pattern(ind + 1, len(input))
        a = sum([input[i] * pattern[i] for i in range(len(input))])
        phase.append(get_ones(a))
    return phase

for _ in range(100):
    input = run_phase(input)

pt1 = int(''.join([str(i) for i in input[:8]]))
print(pt1)

# ---- Day 16: Part 2 ----
with open('input.txt', 'r') as file:
    t = file.read().strip()  # Text input
    n = [int(i) for i in t]  # Number input

input = (10_000 * n)[int(t[:7]):]
for _ in range(100):
    for i in range(len(input) - 1, 0, -1):  # Sum from bottom of triangle up
        input[i - 1] = (input[i - 1] + input[i]) % 10

pt2 = int(''.join([str(i) for i in input[:8]]))
print(pt2)
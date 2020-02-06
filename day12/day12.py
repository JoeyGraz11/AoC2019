from typing import List
from itertools import combinations
import re

class Moon():
    def __init__(self, pos: List[float]):
        self.pos = pos
        self.vel = [0, 0, 0]

    def __repr__(self):
        return f'{tuple(self.pos)}{tuple(self.vel)},{self.ke},{self.pe}'

    @property
    def pe(self):
        return sum([abs(i) for i in self.pos])

    @property
    def ke(self):
        return sum([abs(i) for i in self.vel])

    @property
    def te(self):
        return self.ke * self.pe

    def apply_velocity(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos[2] += self.vel[2]

    def apply_gravity(self, other: 'Moon'):
        if self.pos[0] > other.pos[0]:
            self.vel[0] -= 1
            other.vel[0] += 1
        elif self.pos[0] < other.pos[0]:
            self.vel[0] += 1
            other.vel[0] -= 1

        if self.pos[1] > other.pos[1]:
            self.vel[1] -= 1
            other.vel[1] += 1
        elif self.pos[1] < other.pos[1]:
            self.vel[1] += 1
            other.vel[1] -= 1

        if self.pos[2] > other.pos[2]:
            self.vel[2] -= 1
            other.vel[2] += 1
        elif self.pos[2] < other.pos[2]:
            self.vel[2] += 1
            other.vel[2] -= 1

# Import data
moons = []
with open('input.txt') as file:
    for moon in file:
        m = re.findall('(?<==)(.*?)(?=[,>])', moon)
        moons.append(Moon([float(m[0]), float(m[1]), float(m[2])]))

# Operate on moons
for i in range(1000):
    for pair in combinations(moons, 2):
        pair[0].apply_gravity(pair[1])
    for moon in moons:
        moon.apply_velocity()


tot = 0
for moon in moons:
    tot += moon.te
print(tot)

# ---- Part 2 ----
moons = []
with open('input.txt') as file:
    for moon in file:
        m = re.findall('(?<==)(.*?)(?=[,>])', moon)
        moons.append(Moon([float(m[0]), float(m[1]), float(m[2])]))

inital_state = [[(m.pos[axis], m.vel[axis]) for m in moons] for axis in range(3)]

ts_dict = {}
# Operate on moons
i = 0
while len(ts_dict) < 3:
    i += 1
    # Apply gravity to all moons
    for pair in combinations(moons, 2):
        pair[0].apply_gravity(pair[1])
    # Use new gravity to apply velocity
    for moon in moons:
        moon.apply_velocity()

    for ind in range(3):
        if ind not in ts_dict and inital_state[ind] == [(m.pos[ind], m.vel[ind]) for m in moons]:
            ts_dict[ind] = i

print(ts_dict)
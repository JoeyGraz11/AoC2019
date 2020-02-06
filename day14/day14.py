from typing import List, Tuple
from math import ceil


class Chemical:
    chemicals = {}
    remainder = {}

    def __init__(self, name, amount, made_by):
        self.name: str = name
        self.amount_made: int = amount
        self.made_by: List[Tuple[int, str]] = made_by

    def __repr__(self):
        return self.name

    def get_ore_cost(self, num_reactions) -> int:
        if self.made_by[0][1] == 'ORE':
            self.remainder['ORE'] = 0
            return self.made_by[0][0] * num_reactions

        total_cost = 0
        for amount_req, input_name in self.made_by:
            amount_req = num_reactions * amount_req

            # If the input is not in the remainder dictionary add it
            if input_name not in self.remainder:
                self.remainder[input_name] = 0

            # If the amount that this input will make is less than or equal to the number of this input that is already
            # stored up do not run the reaction
            if self.chemicals[input_name].amount_made <= self.remainder[input_name]:
                return 0

            num_available = self.remainder[input_name]
            num_to_run = ceil((amount_req - num_available) / self.chemicals[input_name].amount_made)
            total_cost += self.chemicals[input_name].get_ore_cost(num_to_run)
            num_available += self.chemicals[input_name].amount_made * num_to_run

            self.remainder[input_name] = num_available - amount_req

        return total_cost


with open('input.txt', 'r') as file:
    for line in file:
        index = line.find('>') + 1
        output = line[index:].strip().split()
        output[0] = int(output[0])
        inputs = line[:index - 2].strip().split(',')
        inputs = [i.strip().split(' ') for i in inputs]
        inputs = [(int(i[0]), i[1]) for i in inputs]

        chem = Chemical(output[1], output[0], inputs)
        chem.chemicals[output[1]] = chem

# ---- Part 1 ----
fuel_to_ore = Chemical.chemicals["FUEL"].get_ore_cost(1)
print(f'Require {fuel_to_ore} ORE to make 1 FUEl')


# ---- Part 2 ----
target = 1_000_000_000_000

Chemical.remainder = {}

min = 0
max = 10_000_000
mid = ceil(0.5 * (min + max))
last = 0
i = 0
while i < 1000:
    Chemical.remainder = {}
    ore_cost = Chemical.chemicals["FUEL"].get_ore_cost(mid)
    #print(f'Iteration: {i}, FUEL: {mid}, ORE: {ore_cost}')
    if ore_cost == last:
        if ore_cost > target:
            mid -= 1
        break
    elif ore_cost > target:
        max = mid
    elif ore_cost < target:
        min = mid
    else:
        break

    last = ore_cost
    mid = ceil(0.5 * (min + max))
    i += 1

Chemical.remainder = {}
print(f'You can produce {mid} FUEL with {target} ORE.')
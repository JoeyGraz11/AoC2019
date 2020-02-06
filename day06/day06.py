from typing import List


class Planet:
    def __init__(self, name: str = 'COM', orbits: str = 'None'):
        self.name: str = name
        self.orbits: str = orbits
        self.orbited: List['Planet'] = []

    def add_orbiter(self, other: 'Planet') -> bool:
        # Add to orbited list
        if other.orbits == self.name:
            self.orbited.append(other)
            return True
        # Or orbited list of an orbiting planet
        for ob in self.orbited:
            if ob.add_orbiter(other):
                return True
        # Else
        return False

    def get_system(self) -> List[str]:
        ob = [self.name]
        for body in self.orbited:
            ob.extend(body.get_system())
        return ob

    def get_system_count(self, count: int) -> int:
        cnt = count
        for ob in self.orbited:
            cnt = cnt + ob.get_system_count(count + 1)
        return cnt

    def is_child(self, other: str) -> int:
        # Return 0 if other is not in hirearchy
        for ob in self.orbited:
            if ob.name == other:
                return 1
            dist = ob.is_child(other)
            if dist > 0:
                return dist + 1
        return 0

    def get_common_parent(self, p1: str, p2: str):
        next = None
        for ob in self.orbited:
            if p1 not in ob.get_system() or p2 not in ob.get_system():
                continue
            if p1 in ob.get_system() and p2 in ob.get_system():
                next = ob
        if next:
            parent = next.get_common_parent(p1, p2)
            if parent:
                return parent
            else:
                return None
        else:
            return self

    def __repr__(self):
        return '-'.join(self.get_system())


class SolarSystem:
    planets: List[Planet] = [Planet(name='COM', orbits='None')]

    def add_planet(self, other: Planet) -> bool:
        if other.name == 'COM':  # If we are trying to re-add the root planet just return
            return False

        # If was a previously orphaned planet remove from the planets list to prepare for re-insertion
        if other in self.planets:
            self.planets.remove(other)

        # If the planet I orbit is not contained in top level list then
        # add me to the top level list as an orphaned planet
        if other.orbits not in self.planet_names:
            self.planets.append(other)
            return False

        # Else I know my parent planet is contained somewhere in the planets hierarchy
        # Loop through the planet list and try to add me as a child
        for planet in self.planets:
            if planet.add_orbiter(other):
                # When I am successfuly added as a child to a planet in the list
                # Then try to re-insert that planet back into the list
                # Sort of a recursive way to build any more connections that have become possible
                self.add_planet(planet)
                return True

        return False

    def clean_planets(self):
        # Loop over planets and just try to re-add them
        # Idea is to remove from top level list and hopefully have planet placed under a parent planet somewhere
        if len(self.planets) == 1:
            return
        num_before = len(self.planets)
        for planet in self.planets:
            self.add_planet(planet)
        if len(self.planets) < num_before:
            self.clean_planets()

    @property
    def planet_names(self) -> List[str]:
        ob = []
        for planet in self.planets:
            ob.extend(planet.get_system())
        return ob

    @property
    def orbit_checksum(self) -> int:
        self.clean_planets()
        count = 0
        for planet in self.planets[0].orbited:
            count = count + planet.get_system_count(count + 1)
        return count

    def num_orbits_to(self, other: str) -> int:
        # Number of orbits from CoM to given planet
        self.clean_planets()
        return self.planets[0].is_child(other)

    def num_orbits_between(self, p1: str, p2: str) -> int:
        self.clean_planets()
        common_parent = self.planets[0].get_common_parent(p1, p2)
        d1 = common_parent.is_child(p1)
        print(f'The distance to {p1} from {common_parent.name} is: {d1}')
        d2 = common_parent.is_child(p2)
        print(f'The distance to {p2} from {common_parent.name} is: {d2}')
        return d1 + d2 - 2

with open('input.txt', 'r') as file:
    ss = SolarSystem()
    for i, line in enumerate(file):
        system = line.strip().split(')')
        new_planet = Planet(system[1], system[0])
        ss.add_planet(new_planet)
        print(f'Added planet #{i}: {system[1]}')

    print(f'The orbit checksum is: {ss.orbit_checksum}')
    p1 = 'YOU'
    p2 = 'SAN'
    print(f'The number of orbits between {p1} and {p2} is: {ss.num_orbits_between(p1, p2)}')
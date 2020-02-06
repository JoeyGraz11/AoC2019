import math

# ---- Part 1 ----
asteroids = []
with open('input.txt') as file:
    for y, line in enumerate(file):
        for x, char in enumerate(line.strip()):
            asteroids.append((char, (x, y)))


def dist(dx, dy):
    return dx**2 + dy**2


max_visible = [0, (0, 0), {}]
for self in asteroids:
    angles = {}
    if self[0] != '#':
        continue
    for other in asteroids:
        if self == other:
            continue
        if other[0] != '#':
            continue

        diff_x = other[1][0] - self[1][0]
        diff_y = other[1][1] - self[1][1]

        angle = 0

        if diff_y > 0:
            if diff_x > 0:  # Other is bottom right
                angle = math.atan(diff_y / diff_x)
            elif diff_x < 0:  # Other is bottom left
                angle = -math.atan(diff_y / diff_x) + 3.14159 / 2
            elif diff_x == 0:
                angle = 3.14159 / 2
        elif diff_y < 0:
            if diff_x > 0:  # Other is top right
                angle = math.atan(diff_y / diff_x)
            elif diff_x < 0:  # Other is top left
                angle = -math.atan(diff_y / diff_x) - 3.14159 / 2
            elif diff_x == 0:
                angle = -3.14159 / 2
        elif diff_y == 0:
            if diff_x > 0:  # Directly right
                angle = 0
            elif diff_x < 0:  # Directly left
                angle = 3.14159

        if angle in angles:
            inserted = False
            for i, _ in enumerate(angles[angle]):
                if dist(diff_x, diff_y) < angles[angle][i][0]:  # Closer asteroids in the front of the list
                    angles[angle].insert(i, (dist(diff_x, diff_y), other[1]))
                    inserted = True
                    break
            if not inserted:
                angles[angle].append((dist(diff_x, diff_y), other[1]))
        else:
            angles[angle] = [(dist(diff_x, diff_y), other[1])]

    if len(angles) > max_visible[0]:
        max_visible[0] = len(angles)
        max_visible[1] = self[1]
        max_visible[2] = angles

# ---- Part 2 ----

angles = max_visible[2].keys()
top_left = sorted([i for i in angles if i < -3.14159 / 2])
bot_left = sorted([i for i in angles if i >= 3.14159 / 2])
bot_right = sorted([i for i in angles if i < 3.14159 / 2 and i > 0])
top_right = sorted([i for i in angles if i >= -3.14159 / 2 and i <= 0])

ordered_keys = top_right
ordered_keys.extend(bot_right)
ordered_keys.extend(bot_left[::-1])
ordered_keys.extend(top_left[::-1])

popped_count = 0
popped = None
while popped_count < 200:
    for key in ordered_keys:
        if max_visible[2][key]:
            popped = max_visible[2][key].pop(0)
            popped_count += 1
            print(key, popped_count, popped)

        if popped_count == 200:
            break

print(popped)
print(f'{popped[1][0]*100 + popped[1][1]}')
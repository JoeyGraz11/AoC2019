import re

# Inputs
MIN = 168630
MAX = 718098

# Part 1
regex = re.compile(r'(.)\1{1,}')
password_count = 0
for i in range(MIN, MAX + 1):
    s = str(i)
    re_result = regex.findall(s)
    if not re_result:
        continue

    cur_digit = int(s[0])
    passing = True
    for digit in s[1:]:
        digit = int(digit)
        if cur_digit - digit > 0:
            passing = False
        cur_digit = digit

    if passing:
        password_count += 1

print(password_count)

# Part 2
regex = re.compile(r'(.)\1{1,}')
regex2 = re.compile(r'(.)\1{2,}')
password_count = 0
for i in range(MIN, MAX + 1):
    s = str(i)
    re_result = regex.findall(s)
    if not re_result:
        continue

    re_result2 = regex2.findall(s)
    if re_result2 and (len(re_result) <= 1 or len(re_result2) >= 2):
        continue

    cur_digit = int(s[0])
    passing = True
    for digit in s[1:]:
        digit = int(digit)
        if cur_digit - digit > 0:
            passing = False
        cur_digit = digit

    if passing:
        password_count += 1

print(password_count)
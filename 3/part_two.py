#!/bin/env python3
import re

with open('input') as f:
    data = f.read()

r = r'(do\(\))|(don\'t\(\))|mul\((\d+),(\d+)\)'

res = re.findall(r, data)
#print(res)

res2 = [list(filter(None, x)) for x in res]

mult = True
total = 0

for el in res2:
    if len(el) == 1:
        mult = el[0] == "do()"
        continue
    if mult:
        total += int(el[0]) * int(el[1])

print(total)

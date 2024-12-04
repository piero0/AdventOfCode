#!/bin/env python3
import re

with open('input') as f:
    data = f.read()

res = re.findall(r'mul\((\d+),(\d+)\)', data)
print(sum([int(a)*int(b) for a,b in res]))


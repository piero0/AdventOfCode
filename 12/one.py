#!/usr/bin/env python3
import sys

def match_pattern(pat, req):
    groups = []
    group_size = 0
    for c in pat:
        if c == '#':
            group_size += 1
        elif group_size > 0:
            groups.append(group_size)
            group_size = 0
    if group_size > 0:
        groups.append(group_size)
    # print(f'{pat} {groups} {req}')
    return int(groups == req)

def fill_pattern(pat, bin_str):
    bin_str = bin_str.replace('0', '.')
    bin_str = bin_str.replace('1', '#')
    for i in range(len(bin_str)):
        pat = pat.replace('?', bin_str[i], 1)
    return pat

def solve(line):
    pat, req = line.split(' ')
    req = list(map(int, req.split(',')))

    ''' I'm way behind on AoC, so I'm just going to brute force this one
        as inputs are relatively small.
        But let's take a moment to look for a more efficient solution :)
        ok so for the today we're going for the brute force :)
    '''

    c = pat.count('?')
    total = 0
    for i in range(2**c):
        bin_str = str(bin(i))[2:].zfill(c)
        prop = fill_pattern(pat, bin_str)
        total += match_pattern(prop, req)

    # print(f'{c} {2**c} {total}')
    return total

def main():
    with open(sys.argv[1]) as f:
        data = f.read().splitlines()
    total = 0
    for line in data:
        total += solve(line)
    print(total)

if __name__ == "__main__":
    main()

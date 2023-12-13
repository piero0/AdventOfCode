#!/usr/bin/env python

def extrapolate(nums):
    prev = 0
    for r in reversed(nums):
        # print(prev)
        prev = r[-1] + prev
    return prev

def extrapolate_front(nums):
    prev = 0
    for r in reversed(nums):
        prev = r[0] - prev
    return prev

def parse(nums):
    levels = [nums]
    lvl = 0
    while True:
        row = []
        level = levels[lvl]
        all_zero = True
        for i in range(0, len(level)-1):
            nval = level[i+1] - level[i]
            if nval != 0:
                all_zero = False
            row.append(nval)
        if all_zero:
            break
        levels.append(row)
        lvl+=1

    # print(levels)
    return levels

def main():
    with open('input.txt') as f:
        data = f.readlines()
    
    nums = []

    for l in data:
        nums.append(list(map(int, l.split())))

    tot = 0
    for n in nums:
        tot += extrapolate_front(parse(n))

    print(tot)

main()

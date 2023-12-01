#!/usr/bin/env python

def get_number(line):
    l,r = None, None
    for c in line:
        if c.isnumeric():
            if l is None:
                l = c
            else:
                r = c
    if r is None:
        r = l
    return int(f'{l}{r}')

def match_word(idx, line):
    nums = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}
    for k in nums:
        if line.find(k, idx, idx+len(k)) != -1:
            return nums[k]

def get_number_2(line):
    l, r, tmp = None, None, None
    for i, c in enumerate(line):
        if c.isnumeric():
            tmp = c
        elif tmp := match_word(i, line):
            pass

        if tmp is not None:
            if l is None:
                l = tmp
            else:
                r = tmp
            tmp = None

    if r is None:
        r = l
    return int(f'{l}{r}')

def main():
    with open('input.txt') as f:
        data = f.readlines()

    sum_ = 0

    for l in data:
        sum_ += get_number_2(l)

    print(sum_)

#print(get_number_2('95btwo'))
main()

#!/bin/env python3

def get_next(n):
    if n == 0:
        return [1]
    elif len(str(n)) % 2 == 0:
        ns = str(n)
        m = len(ns) // 2
        a, b = ns[:m], ns[m:]
        return [int(a), int(b)]
    else:
        return [n*2024]

def get_length(nums, nexts, lvl):
    for _ in range(lvl):
        # print('>>next')
        numlist = [k for k in nums if nums[k] > 0]
        updates = {}

        for k in numlist:
            if nums[k] <= 0:
                continue
            if k not in nexts:
                tmp = get_next(k)
                nexts[k] = tmp

            v = nums[k]
            # print(f'k {k}={v} -= {v}')
            # print(f'v {v} nexts {nexts[k]}')

            for n in nexts[k]:
                if n not in updates:
                    updates[n] = 0
                updates[n] += v

            nums[k] -= v

        for k,v in updates.items():
            if k not in nums:
                nums[k] = 0
            nums[k] += v

        to_remove = []
        for k,v in nums.items():
            if v <= 0:
                to_remove.append(k)
        for k in to_remove:
            nums.pop(k)

        #print(f'keynum {len(nums.keys())}')
    return sum([v for v in nums.values()])

def skip0(nums):
    d = {}
    for k,v in nums.items():
        if v > 0:
            d[k] = v
    return d

def main():
    file = '../data/2024/11/input'
    # file = '../data/2024/11/test_input'

    with open(file) as f:
        data = f.read().strip().split()

    nexts = {}
    nums = {int(k):1 for k in data}
    print(nums)
    i = 75
    l = get_length(nums, nexts, i)
    print(l)

main()

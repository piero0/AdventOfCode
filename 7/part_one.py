#!/bin/env python3
from itertools import product

def check_all(s, n):
    lenn = len(n)-1
    ops_prod = product([0, 1], repeat=lenn)
    for ops in ops_prod:
        #print(f'ops {ops}')
        r = n
        #print(f'info {s} {r} {ops}')
        acc = 0
        for i in range(len(ops)):
            op = ops[i]
            #print(f'op {"+" if op == 0 else "*"}')
            if op == 0: # +
                acc = r[0] + r[1]
            else: # *
                acc = r[0] * r[1]
            r = [acc] + r[2:]
        #print(f'out {r}')
        res = sum(r)
        #print(f'!!!sum {res}')
        if res == s:
            #print(f'ok {s}')
            return s
    return 0

def main():
    fname = "../data/2024/7/test_input"
    with open(fname) as f:
        data = f.readlines()

    nums = []
    for l in data:
        l = l.split(':')
        s = int(l[0])
        n = list(map(int, l[1].split()))
        nums.append((s,n))

    total = 0
    for s,n in nums:
        total += int(check_all(s, n))
    print(total)

main()

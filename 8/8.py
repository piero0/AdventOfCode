#!/usr/bin/env python
''' It took like 3min to rewrite this in python
    it's 3x shorter but the output was the same
    which forced me to read the puzzle's description
    more carefully. In the end c++ solution is fixed
    by starting on AAA not on the 1st line :)
'''
from itertools import cycle

def main():
    with open('input.txt') as f:
        lines = f.readlines()

    moves = lines[0].strip()

    m = {}
    first = None
    for l in lines[2:]:
        a,b = l.split('=')
        lr = b.split(',')
        l = lr[0][2:].strip()
        r = lr[1][:-2].strip()
        m[a.strip()] = (l, r)
        if first is None:
            first = a.strip()

    print(m)
    cur = first
    steps = 0
    for mv in cycle(moves):
        # print(mv)
        idx = 0 if mv == 'L' else 1
        nxt = m[cur][idx]
        steps+=1
        if nxt == 'ZZZ':
            break
        cur = nxt
    print(steps)

main()

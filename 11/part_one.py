#!/usr/bin/env python

def parse_galaxy(data):
    cols = [True] * (len(data[0])-1)
    rows = []
    y = 0
    glx = []
    for row in data:
        rows.append(True)
        for x,c in enumerate(row.strip()):
            if c != '.':
                cols[x] = False
                rows[y] = False
                glx.append([x, y])
        y+=1
    return glx, rows, cols

def expand(glx, s, sort_key):
    glx.sort(key=lambda x: x[sort_key])

    gaps = []
    tmp = 0
    for i,s in enumerate(s):
        if s:
            tmp += 1
            gaps.append((i, tmp))
    
    # print(f'gaps {sort_key} {gaps}')
    key = sort_key
    # print(f'key {key}')

    import copy

    for i in range(len(glx)):
        p = glx[i][key]
        prev = copy.copy(glx[i])
        for gap in gaps:
            g = gap[0]
            if p > g:
                glx[i][key] += 1000000-1
        # print(f'{i}.{key} {prev} -> {glx[i]}')

    return glx

def dist(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])

def get_distance(glx):
    size = len(glx)
    total = 0
    n = 0
    for i in range(size):
        for j in range(i, size):
            dst = dist(glx[i], glx[j])
            # print(f'{i}x{j}={dst} {glx[i]} {glx[j]}')
            total += dst
            n+=1

    # print(f'{size} {n} {(size*size-size)/2}')
    return total

import sys

def main():
    with open(sys.argv[1]) as f:
        data = f.readlines()
    g, r, c = parse_galaxy(data)
    # print(f'{r}\n{c}\n{g}\n')
    exp = expand(g, c, 0)
    exp2 = expand(exp, r, 1)
    print(get_distance(exp2))

main()

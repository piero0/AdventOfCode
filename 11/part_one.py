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
    
    print(f'gaps {sort_key} {gaps}')

    si = 0
    gi = 0

    key = sort_key

    while True:
        if gi >= len(glx):
            break

        g = glx[gi]
        s = gaps[si]

        if g[key] < s[0]:
            gi+=1
            continue

        # more spaces
        if si+1 < len(gaps):
            nexts = gaps[si+1]
            if g[key] < nexts[key]:
                g[key] += s[1]
                gi+=1
            else:
                si+=1
        else: #last space
            g[key] += s[1]
            gi+=1

    return glx

def dist(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])

def get_distance(glx):
    size = len(glx)
    total = 0
    n = 0
    for i in range(size):
        for j in range(i+1, size):
            dst = dist(glx[i], glx[j])
            print(f'{i}x{j}={dst} {glx[i]} {glx[j]}')
            total += dst
            n+=1

    print(f'{size} {n} {(size*size-size)/2}')
    return total

def main():
    with open('input.txt') as f:
        data = f.readlines()
    g, r, c = parse_galaxy(data)
    g.sort(key=lambda x: x[0])
    print(f'{r}\n{c}\n{g}\n')
    exp = expand(g, c, 0)
    print(exp)
    exp = expand(exp, r, 1)
    print(exp)
    print(get_distance(exp))

main()
# 9285282 too low

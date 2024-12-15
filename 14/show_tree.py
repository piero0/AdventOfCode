#!/bin/env python3

MAXX = 101
MAXY = 103

def parseData(line):
    line = line.strip()
    a,b = line.split()
    axy = list(map(int, a[2:].split(',')))
    bxy = list(map(int, b[2:].split(',')))
    return (axy, bxy)

def step(i, pts):
    new = []
    for (s,v) in pts:
        nx = (s[0] + i*v[0]) % MAXX
        ny = (s[1] + i*v[1]) % MAXY
        new.append((abs(nx), abs(ny)))
    return new

def countPts(pts):
    mx = MAXX // 2
    my = MAXY // 2
    qd = [0,0,0,0]
    # print(mx,my)
    # print(pts)
    for x,y in pts:
        if x == mx or y == my:
            continue
        idx = 0 if x < mx else 1
        idx += 0 if y < my else 2
        # print(x,y,idx)
        qd[idx] += 1

    # print(qd)
    total = 1
    for q in qd:
        total *= q
    return total

def printPts(pts):
    ar = [['.' for _ in range(MAXX)] for _ in range(MAXY)]

    for p in pts:
        ar[p[1]][p[0]] = 'x'

    maxc = 0
    for r in ar:
        xc = r.count('x')
        if xc > maxc:
            maxc = xc
    print(maxc)

    print('\n'.join([''.join(r) for r in ar]))

def main():
    with open('../data/2024/14/input') as f:
        data = f.readlines()

    pts = [parseData(l) for l in data]

    # step100 = step(100, pts)
    # print(countPts(step100))

    # for a in range(1,10000):
    #     printPts(step(a, pts))

    printPts(step(7338, pts))

main()

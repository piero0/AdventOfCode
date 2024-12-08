#!/bin/env python3
import itertools as it

def find_points(ants, mxy):
    #print(ants)
    pairs = it.combinations(ants, 2)

    out = []
    if len(ants) > 1:
        out.extend(ants)

    for a,b in pairs:
        #print('in', a,b)
        d = (a[0]-b[0], a[1]-b[1])
        #print('new', a2, b2)

        ap = a
        while True:
            a2 = (ap[0]+d[0], ap[1]+d[1])
            if a2[0] >= 0 and a2[0] < mxy[0] and a2[1] >= 0 and a2[1] < mxy[1]:
                out.append(a2)
            else:
                break
            ap = a2

        bp = a
        while True:
            b2 = (bp[0]-d[0], bp[1]-d[1])
            if b2[0] >= 0 and b2[0] < mxy[0] and b2[1] >= 0 and b2[1] < mxy[1]:
                out.append(b2)
            else:
                break
            bp = b2

    #print('out', out)
    return out

def main():
    file = '../data/2024/8/input'
    with open(file) as f:
        data = f.readlines()

    d = {}
    y = 0
    x = 0
    for l in data:
        for c in l[:-1]:
            if c != '.':
                el = d.setdefault(c, [])
                el.append((x,y))
            x+=1
        x=0
        y+=1

    #print(d)

    mxy = (len(data[0])-1, len(data))
    #print(mxy)

    points = set()
    for a in d:
        pts = find_points(d[a], mxy)
        for p in pts:
            points.add(p)

    #print(points)
    print(len(points))

main()

#!/bin/env python3

def onmaze(p, maxy):
    return p[0] >= 0 and p[0] < maxy[0] and p[1] >= 0 and p[1] < maxy[1]

def walk(start, maze):
    maxy = (len(maze[0]), len(maze))
    ss = [(start, 0)]
    vis = set()
    total = 0

    while len(ss) > 0:
        s, v = ss.pop()

        if s in vis:
            continue

        for d in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            ns = (s[0]+d[0], s[1]+d[1])
            if not onmaze(ns, maxy):
                continue
            if ns in vis:
                continue
            nv = maze[ns[1]][ns[0]]
            if v + 1 == nv:
                if nv == 9:
                    total += 1
                    vis.add(ns)
                ss.append(((ns[0],ns[1]), nv))

        vis.add(s)
    return total

def main():
    file = '../data/2024/10/input'
    with open(file) as f:
        data = f.readlines()

    data = map(lambda x: x.strip(), data)
    data = list(map(lambda x: [int(n) for n in x], data))

    starts = set()
    for y in range(len(data)):
        for x in range(len(data[0])):
            if data[y][x] == 0:
                starts.add((x,y))

    total = 0
    for s in starts:
        total += walk(s, data)

    print('total:', total)

main()

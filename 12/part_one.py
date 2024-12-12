#!/bin/env python3

class Pt:
    dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    maxs = []

    def __init__(self, xy, c):
        self.xy = xy
        self.c = c

    def __add__(self, xy):
        if isinstance(xy, Pt):
            xy = xy.xy
        return Pt((self.xy[0] + xy[0], self.xy[1] + xy[1]), self.c)

    def __iadd__(self, xy):
        self.xy = (self.xy[0] + xy[0], self.xy[1] + xy[1])
        return self

    def on_grid(self):
        return self.xy[0] >= 0 and self.xy[0] < Pt.maxs[0] and self.xy[1] >= 0 and self.xy[1] < Pt.maxs[1]

    def __repr__(self):
        return f'{self.c} {self.xy}'

    def __eq__(self, o):
        return self.xy == o.xy and self.c == o.c

    def __hash__(self):
        return hash((self.xy, self.c))

    def get_nb(self, data):
        nb = []
        for d in Pt.dirs:
            np = self + d
            if not np.on_grid():
                continue
            nc = data[np.xy[1]][np.xy[0]]
            if self.c == nc:
                nb.append(np)
        return nb

    def check(self, grid):
        p = 0
        for d in Pt.dirs:
            np = self + d
            if not np.on_grid() or grid[np.xy[1]][np.xy[0]] != self.c:
                p += 1
        return p

def get_grp_score(g, data):
    c = '?'
    for p in g:
        c = p.c
        break
    p = sum([p.check(data) for p in g])
    a = len(g)
    # print(f'c {c} a {a} p {p} t {a*p}')
    return a,p

def add_to_group(newgrp, grps):
    # print(f'lengrps {len(grps)}')
    # print(grps)
    matches = set()
    for i in range(len(grps)):
        for p in newgrp:
            if p in grps[i]:
                # print(f'match {i}')
                matches.add(i)

    lm = len(matches)
    # print(f'lenmatch {lm}')
    if lm == 0:
        # print('newgrp')
        grps.append(newgrp)
    elif lm == 1:
        # print(f'union {matches}')
        m = matches.pop()
        grps[m] = grps[m].union(newgrp)
    else:
        # print(f'multi union: {matches}')
        m = newgrp
        for i in matches:
            # print(f'ug {grps[i]}')
            m = m.union(grps[i])
            grps[i] = set()
        grps.append(m)

def main():
    file = '../data/2024/12/test_input1'
    file = '../data/2024/12/input'
    with open(file) as f:
        data = f.readlines()
    data = [l.strip() for l in data]

    Pt.maxs = [len(data[0]), len(data)]

    grps = []

    for y in range(len(data)):
        for x in range(len(data[0])):
            s = data[y][x]
            # if s != 'C':
            #     continue
            p = Pt((x, y), s)

            nb = p.get_nb(data)
            newgrp = set(nb)
            newgrp.add(p)
            # print(f'> p {p} nb {newgrp}')
            add_to_group(newgrp, grps)

    total = 0
    for g in grps:
        a,p = get_grp_score(g, data)
        total += a*p
    print(total)

main()

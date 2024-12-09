#!/bin/env python3
import copy

def fill_gap(gs, data):
    fill = []
    pop = 0
    while gs > 0:
        i,s = data[-1]
        ngs = gs - s
        if ngs == 0:
            fill.append((i,s))
            data.pop()
            pop+=1
        elif ngs < 0:
            fill.append((i, gs))
            data[-1] = (i, s - gs)
        else:
            fill.append((i, s))
            data.pop()
            pop+=1
        gs -= s
    #print(f'fill {fill} pop {pop}')
    #print(f'filler {data}')
    return fill

def should_stop(last, next):
    return last[0] == next[0]

def rearrange(data):
    fillers = list(filter(lambda e: e[0]>=0, copy.copy(data)))
    gaps = list(filter(lambda e: e[0]<0, copy.copy(data)))

    out = []
    pos = 0
    for i,s in data:
        #print(f'rearr {i},{s}')
        if i >= 0:
            #print(f'pass {i},{s}')
            out.append((i,s))
        else:
            #print(f'gap {i},{s}')
            fill = fill_gap(s, fillers)
            out.extend(fill)
        if should_stop(out[-1], data[pos+1]):
             out.append(fillers[-1])
             #print('end')
             break
        pos += 1

    return out

def checksum(nodes):
    total = 0
    pos = 0
    for nd in nodes:
        for _ in range(nd[1]):
            total += pos * nd[0]
            pos += 1
    return total

def main():
    # file = '../data/2024/9/test_input'
    file = '../data/2024/9/input'

    with open(file) as f:
        data = f.read()
    data = data.strip()

    bid = 0
    free = False
    data_nodes = []

    for c in data:
        c = int(c)
        if free:
            if c != 0:
                data_nodes.append((-bid, c))
        else:
            data_nodes.append((bid, c))
            bid += 1
        free = not free

    new_nodes = rearrange(data_nodes)
    chksum = checksum(new_nodes)

    #print(data_nodes)
    #print(new_nodes)
    print(chksum)

main()

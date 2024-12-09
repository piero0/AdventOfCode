#!/bin/env python3

def rearrange(data):
    end_idx = -1
    beg_idx = 0
    while True:
        if len(data)+end_idx < 0:
            # print('end')
            break

        last = data[end_idx]

        if beg_idx >= len(data)+end_idx:
            beg_idx = 0
            end_idx -= 1

        space = data[beg_idx]
        # print(f'>> bi: {beg_idx} ei: {end_idx} l: {last} s: {space}')

        if last[0] < 0:
            end_idx -= 1
            continue

        if space[0] >= 0:
            beg_idx += 1
            continue

        diff = space[1] - last[1]
        # print(f'd {diff}')
        if diff >= 0:
            data[beg_idx] = last
            if diff > 0:
                data.insert(beg_idx+1, (space[0], diff))
            data[end_idx] = (-1, last[1])
            beg_idx = 0
        else:
            beg_idx += 1

        # print('ND', data)

    return data

def checksum(nodes):
    total = 0
    pos = 0
    for nd in nodes:
        for _ in range(nd[1]):
            if nd[0] >= 0:
                total += pos * nd[0]
            pos += 1
    return total

def main():
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
    print(chksum)

main()

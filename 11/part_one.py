#!/bin/env python3

def go(data):
    new = []
    for n in data:
        if n == '0':
            new.append('1')
        elif len(n) % 2 == 0:
            m = len(n) // 2
            a,b = n[:m], n[m:]
            new.extend([a,str(int(b))])
        else:
            new.append(str(int(n)*2024))
    return new

def main():
    file = '../data/2024/11/input'

    with open(file) as f:
        data = f.read().strip().split()

    I = 25
    for _ in range(I):
        # print('before', data)
        data = go(data)
        # print('after', data)

    # print(data)
    print(len(data))

main()

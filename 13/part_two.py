#!/bin/env python3

def convert_line(line):
    return [int(l[3:]) for l in line.split(':')[1].split(',')]

def read_data(data):
    bn = 10_000_000_000_000
    out = []
    for i in range(0, len(data), 4):
        a = convert_line(data[i])
        b = convert_line(data[i+1])
        p = convert_line(data[i+2])
        p = [p[0] + bn, p[1] + bn]
        out.append((a,b,p))
    return out

def solve(l):
    a, b, p = l
    ax, ay = a
    bx, by = b
    px, py = p

    A = ax
    B = bx
    C = px
    D = ay
    E = by
    F = py

    b = (D*C - A*F)/(-A * E + D*B)
    a = (F - b*E) / D
    # print(a,b)
    if a.is_integer() and b.is_integer():
        return int(a*3 + b)

    return 0

def main():
    # file = '../data/2024/13/test_input'
    file = '../data/2024/13/input'
    with open(file) as f:
        data = f.readlines()
    data = [d.strip() for d in data]
    o = read_data(data)

    total = 0
    for l in o:
        total += solve(l)
    print(total)

main()

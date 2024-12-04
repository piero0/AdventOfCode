#!/bin/env python3
'''
 M_S M_M
 _A_ _A_
 M_S S_S

 S_M S_S
 _A_ _A_
 S_M M_M
'''

def verify_x(y, x, data):
    tl = data[y][x]
    tr = data[y][x+2]
    m = data[y+1][x+1]
    bl = data[y+2][x]
    br = data[y+2][x+2]

    pat = ''.join([tl,tr,m,bl,br])
    sols = ['MSAMS', 'MMASS', 'SMASM', 'SSAMM']

    return pat in sols

def count_xmas(data):
    total = 0

    for y in range(len(data)-2):
        for x in range(len(data[0])-3):
            #print(y,x)
            if verify_x(y, x, data):
                total += 1

    return total

def main():
    puzzle_input = 'input'
    with open(puzzle_input) as f:
        data = f.readlines()
    print(count_xmas(data))

main()

#!/bin/env python3

def build_word_diag1(y, x, data):
    return f'{data[y][x]}{data[y+1][x+1]}{data[y+2][x+2]}{data[y+3][x+3]}'

def build_word_diag2(y, x, data):
    return f'{data[y+3][x]}{data[y+2][x+1]}{data[y+1][x+2]}{data[y][x+3]}'

def build_word_vert(y, x, data):
    return f'{data[y][x]}{data[y+1][x]}{data[y+2][x]}{data[y+3][x]}'


def count_xmas(data):
    total = 0
    words = ['XMAS','SAMX']

    # get horizontal
    for line in data:
        for i in range(len(line)-3):
            if line[i:i+4] in words:
                total += 1

    # get vertical
    for y in range(len(data)-3):
        for x in range(len(data[0])):
            #print(y,x)
            if build_word_vert(y, x, data) in words:
                total += 1

    # get diagonal
    for y in range(len(data)-3):
        for x in range(len(data[0])-3):
            if build_word_diag1(y, x, data) in words:
                total += 1
            if build_word_diag2(y, x, data) in words:
                total += 1

    return total

def main():
    puzzle_input = 'input'
    with open(puzzle_input) as f:
        data = f.readlines()
    print(count_xmas(data))

main()

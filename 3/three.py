#!/usr/bin/env python

def is_symbol(c):
    return not (c.isnumeric() or c == '.')

def check_line(start, end, idx, lines):
    range_start = start-1 if start >= 1 else 0
    status = [is_symbol(c) for c in lines[idx][range_start:end+2]]
    #print(status)
    return any(status)

def get_digits(line):
    digit = ''
    start = -1
    end = -1
    digits = []
    for i,c in enumerate(line):
        if c.isnumeric():
            digit += c
            if start < 0:
                start = i
            else:
                end = i
        elif start > -1:
            if end == -1:
                end = start
            digits.append(((start, end), int(digit)))
            start = end = -1
            digit = ''
    if digit != '':
        if end == -1:
            end = start
        digits.append(((start, end), int(digit)))
    #print(digits)
    return digits

def check_adjacent(digit_struct, lines):
    (start, end), digit = digit_struct
    # print(len(lines))
    # current line

    range_start = start-1 if start >= 1 else 0 
    new_end = is_symbol(lines[1][end+1]) if end+1 < len(lines[1]) else False
    cl = any([is_symbol(lines[1][range_start]), new_end])
    #print(cl)
    pl = check_line(start, end, 0, lines)
    nl = check_line(start, end, 2, lines)

    print()
    print(f'{lines[0][range_start:end+2]} {pl}')
    print(f'{lines[1][range_start:end+2]} {cl}')
    print(f'{lines[2][range_start:end+2]} {nl}')

    if any([cl, pl, nl]):
        print(f'{digit} OK\n')
        return digit
    else:
        print(f'{digit} NOK\n')
        return 0

def main():
    with open('3/input.txt') as f:
        data = f.readlines()

    filler = ['.' * len(data[0])]

    nonewlines = [x[:-1] for x in data]

    lines = filler + nonewlines + filler

    sum_ = 0

    for i in range(1, len(lines)-1):
        print(i, lines[i])
        digs = get_digits(lines[i])
        print(digs)
        for d in digs:
            sum_ += check_adjacent(d, lines[i-1:i+2])
        # break

    print('\n', sum_)

main()

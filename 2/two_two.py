#!/usr/bin/env python

def parse_line(l):
    max_ = {'red': 0, 'green': 0, 'blue': 0}
    id_, games = l.split(':')
    id_ = id_.split()[1]

    for g in games.split(';'):
        for c in g.split(','):
            count, color = c.split()
            max_[color] = max(int(count), max_[color])

    return max_['red'] * max_['green'] * max_['blue']

def main():
    with open('input.txt') as f:
        data = f.readlines()

    sum_ = 0
    for l in data:
        sum_ += parse_line(l)
    
    print(sum_)

main()

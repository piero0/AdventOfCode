#!/usr/bin/env python

def parse_line(l):
    max_ = {'red': 12, 'green': 13, 'blue': 14}
    id_, games = l.split(':')
    id_ = id_.split()[1]

    for g in games.split(';'):
        for c in g.split(','):
            count, color = c.split()
            if int(count) > max_[color]:
                return 0

    return int(id_)

def main():
    with open('input.txt') as f:
        data = f.readlines()

    sum_ = 0
    for l in data:
        sum_ += parse_line(l)
    
    print(sum_)

main()

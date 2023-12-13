#!/usr/bin/env python
import enum

def parse_maze(data):
    return [l.strip() for l in data]

class D(enum.Enum):
    N = 0
    W = 1
    E = 2
    S = 3

def get_dir(from_, to):
    fy, fx = from_
    ty, tx = to

    dy = fy - ty
    dx = fx - tx

    y = D.S if dy < 0 else D.N
    x = D.E if dx < 0 else D.W
    return y if dx == 0 else x

def get_next_step(pos, d, maze):
    y,x = pos
    c = maze[y][x]
    dt = (0, 0)

    match c:
        case '|':
            dt = (-1, 0) if d == D.N else (1, 0)
        case '-':
            dt = (0, -1) if d == D.W else (0, 1)
        case 'L':
            dt = (-1, 0) if d == D.W else (0, 1)
        case 'J':
            dt = (0, -1) if d == D.S else (-1, 0)
        case '7':
            dt = (0, -1) if d == D.N else (1, 0)
        case 'F':
            dt = (0, 1) if d == D.N else (1, 0)

    return (y+dt[0], x+dt[1])

def solve(maze):
    # let's go for a caveman brute force solution ;)
    # assumption:
    # while on the loop there is no crossroads

    #get S location
    S = (-1, -1)
    for i,l in enumerate(maze):
        if (col := l.find('S')) >= 0:
            S = (i, col)

    print(S)

    # cheat :) we know we are going S
    direction = D.S
    pos = (S[0]+1, S[1])

    # have a walk
    length = 1
    # pos = S
    while True:
        pos = get_next_step(pos, direction, maze)
        if pos == S:
            break
        length += 1

    # todo: check do we need some ceil or +1
    return length // 2

def main():
    with open('ex1.txt') as f:
        data = f.readlines()

    maze = parse_maze(data)
    sol = solve(maze)
    print(sol)

main()

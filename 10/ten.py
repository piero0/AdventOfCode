#!/usr/bin/env python
import enum

# direction 'to'
class To(enum.Enum):
    N = (-1, 0)
    W = (0, -1)
    E = (0, 1)
    S = (1, 0)

def move(pos, direction):
    return pos[0]+direction.value[0], pos[1]+direction.value[1]

def get_next_step(pos, d, maze):
    y,x = pos
    c = maze[y][x]
    newd = To.N

    match c:
        case '|':
            newd = d
        case '-':
            newd = d
        case 'L':
            if d == To.W:
                newd = To.N
            elif d == To.S:
                newd = To.E
        case 'J':
            if d == To.E:
                newd = To.N
            elif d == To.S:
                newd = To.W
        case '7':
            if d == To.N:
                newd = To.W
            elif d == To.E:
                newd = To.S
        case 'F':
            if d == To.N:
                newd = To.E
            elif d == To.W:
                newd = To.S

    newpos = move(pos, newd)
    print(c, pos, d, newpos, newd)
    return newpos, newd

def solve(maze):
    # let's go for a caveman brute force solution ;)
    # assumption:
    # while on the loop there is no crossroads

    #get S location
    S = (-1, -1)
    for i,l in enumerate(maze):
        if (col := l.find('S')) >= 0:
            S = (i, col)

    print(S, maze[S[0]][S[1]])

    # cheat :) we know we are going S
    direction = To.S
    pos = (S[0]+1, S[1])

    # have a walk
    length = 1
    while True:
        pos, direction = get_next_step(pos, direction, maze)
        length += 1
        if pos == S:
            break

    return length // 2

def main():
    with open('input.txt') as f:
        data = f.readlines()

    maze = [l.strip() for l in data]
    sol = solve(maze)
    print(sol)

main()

#!/bin/env python3

class Pos:
    def __init__(self, xy):
        self.xy = xy

    def __add__(self, xy):
        newpos = (self.xy[0] + xy[0], self.xy[1] + xy[1])
        return Pos(newpos)

    def __str__(self):
        return f'{self.xy}'

class Dir:
    dirs = [(0,-1), #up
            (1,0), #right
            (0,1), #down
            (-1,0) #left
            ]
    def __init__(self):
        self.current_idx = 0

    def rotate(self):
        self.current_idx += 1
        if self.current_idx >= len(Dir.dirs):
            self.current_idx = 0

    def get(self):
        return Dir.dirs[self.current_idx]

def outside(x, y, maxy):
    return x < 0 or x >= maxy or y < 0 or y >= maxy

def sum_path(path):
    print(''.join([ ''.join(r) + '\n' for r in path]))
    return sum([x == 'X' for r in path for x in r])

def walk(start, grid):
    size = len(grid)
    path = [['.'] * size for _ in range(size)]
    pos = Pos(start)
    _dir = Dir()
    while True:
        x,y = pos.xy
        path[x][y] = 'X'

        newpos = pos + _dir.get()
        x,y = newpos.xy
        if outside(x, y, size):
            print(f'out {x}-{y}')
            break
        elif grid[y][x] == 1:
            print(f'rot {x}-{y}')
            _dir.rotate()
        else:
            print(f'mov {x}-{y}')
            pos = newpos
    return sum_path(path)

def parse_maze(data):
    x,y = 0,0
    size = len(data)
    grid = [[0] * size for _ in range(size)]
    start = (0,0)
    for y in range(len(data)):
        for x in range(len(data[0])-1):
            if data[y][x] == '#':
                grid[y][x] = 1
            elif data[y][x] == '^':
                start = (x,y)
    return start, grid

def main():
    input_text = 'test_input'
    input_text = 'input'
    with open(input_text) as f:
        data = f.readlines()
    start, grid = parse_maze(data)
    print(walk(start, grid))

main()

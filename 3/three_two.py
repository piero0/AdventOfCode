#!/usr/bin/env python

def get_numbers_line(li, ci, lines):
    m = 0
    for c in lines[li][ci-1:ci+2]:
        if c.isnumeric():
            m+=1
    if m == 2:
        if not lines[li][ci].isnumeric():
            return 2
        return 1
    elif m == 3:
        return 1
    return m #0,1

def get_num(txt, left):
    s, e = -1, -1
    sr, er, st = 0, len(txt), 1
    if left:
        sr, er, st = len(txt)-1, -1, -1

    for i in range(sr, er, st):
        if txt[i].isnumeric():
            if s == -1:
                s = i
            else:
                e = i
        else:
            break
    if e == -1:
        e = s
    if left:
        s, e = e, s
    return int(txt[s:e+1])

'''
...
.X.
X..
..X
XX.
.XX
XXX
X.X
'''
def get_one_num(line, ci):
    # get num of digits
    ts = slice(ci-1, ci+2)
    c = list(filter(lambda x: x.isnumeric(), line[ts]))
    lenc = len(c)
    l = line[ts]
    if lenc == 3:
        return int(''.join(c))
    elif lenc == 2:
        p = l.find('.')
        if p == 0:
            return get_num(line[ci:ci+3], left=False)
        else:
            return get_num(line[ci-2:ci+1], left=True)
    elif lenc == 1:
        p = list(map(lambda x: x.isnumeric(), l)).index(True)
        if p == 1:
            return int(l[1])
        elif p == 0:
            return get_num(line[ci-3:ci], left=True)
        elif p == 2:
            return get_num(line[ci+1:ci+4], left=False)


def get_ratio(li, ci, lines):
    cur_left = 1 if lines[li][ci-1].isnumeric() else 0
    cur_right = 1 if lines[li][ci+1].isnumeric() else 0
    up = get_numbers_line(li-1, ci, lines)
    down = get_numbers_line(li+1, ci, lines)

    # print(f'l: {li} {ci}', cur_left, cur_right, up, down)
    mvs = sum([cur_left, cur_right, up, down])
    if mvs != 2:
        return 0

    nums = []
    lslice = slice(ci-3, ci)
    rslice = slice(ci+1, ci+4)

    if cur_left == 1:
        nums.append(get_num(lines[li][lslice], left=True))
    if cur_right == 1:
        nums.append(get_num(lines[li][rslice], left=False))

    if up == 2:
        nums.append(get_num(lines[li-1][lslice], left=True))
        nums.append(get_num(lines[li-1][rslice], left=False))
    elif up == 1:
        nums.append(get_one_num(lines[li-1], ci))

    if down == 2:
        nums.append(get_num(lines[li+1][lslice], left=True))
        nums.append(get_num(lines[li+1][rslice], left=False))
    elif down == 1:
        nums.append(get_one_num(lines[li+1], ci))

    if len(nums) == 1:
        print(f'ERROR {li}')
        print(cur_left, cur_right, up, down)
        print(f'{lines[li-1][ci-1:ci+2]}')
        print(f'{lines[li][ci-1:ci+2]}')
        print(f'{lines[li+1][ci-1:ci+2]}')
    return nums[0]*nums[1] if len(nums) == 2 else 0


def main():
    with open('3/input.txt') as f:
        data = f.readlines()
    
    filler = ['.' * (len(data)+1)]

    newdata = []
    newdata.append(filler)
    for r in data:
        newdata.append('.' + r[:-1] + '.')
    newdata.append(filler)

    sum_ = 0
    for l in range(1, len(newdata)):
        for c in range(1, len(newdata[l])-2):
            if newdata[l][c] == '*':
                sum_ += get_ratio(l, c, newdata)
    print(sum_)

main()

# for test in [('1.3', True), ('.13', True), ('123', True), ('123', False), ('12.', False), ('1.3', False)]:
    # print(get_num(*test))

# for t in [('123', 1), ('123.', 2), ('.123', 1), ('.2.', 1), ('123..', 3), ('..123', 1)]:
    # print(get_one_num(*t))

# 75959030 too low
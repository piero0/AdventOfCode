#!/usr/bin/env python

def to_rank(nums):
    rank = 0
    #five
    if nums[0] == 5:
        rank = 6
    #four
    elif nums[0] == 4:
        rank = 5
    #full
    elif nums[0] == 3 and nums[1] == 2:
        rank = 4
    #three
    elif nums[0] == 3 and nums[1] != 2:
        rank = 3
    #two pair
    elif nums[0] == 2 and nums[1] == 2:
        rank = 2
    #one pair
    elif nums[0] == 2 and nums[1] != 2:
        rank = 1
    #high
    else:
        rank = 0
    return rank

def get_rank(cards):
    d = {}
    for c in cards:
        if c in d:
            d[c] += 1
        else:
            d[c] = 1

    nums = [x for _,x in d.items()]
    nums.sort(reverse=True)

    rank = 0
    if 'J' in d:
        n = d['J']
        if n == 4:
            rank = 6
        elif n == 3: #four or five
            if nums[1] == 2:
                rank = 6
            else:
                rank = 5
        elif n == 2: #four, full, five
            nums.remove(2)
            nums[0] += 2
        elif n == 1: #pair, three, four, five
            nums.remove(1)
            nums[0] += 1 

    if rank == 0:
        rank = to_rank(nums)

    return rank

def mapHand(hand):
    m = {
        'A': '1',
        'K': '2',
        'Q': '3',
        'T': '4',
        '9': '5',
        '8': '6',
        '7': '7',
        '6': '8',
        '5': '9',
        '4': 'a',
        '3': 'b',
        '2': 'c',
        'J': 'd',
        }
    return ''.join([m[x] for x in hand])

def puzzleSort(entry):
    r, c, _ = entry
    return (6-r, mapHand(c))

def main():
    with open('input.txt') as f:
        lines = f.readlines()

    print(len(lines))

    cards = []

    for l in lines:
        hand, bid = l.split(' ')
        cards.append((get_rank(hand), hand, bid.strip()))
    
    cards.sort(key=puzzleSort)
    print(cards)

    total = 0
    rank = len(cards)
    for _,_,b in cards:
        total += int(b) * rank
        rank -= 1
    print(total) 

main()

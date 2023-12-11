#!/usr/bin/env python

def get_rank(cards):
    d = {}
    for c in cards:
        if c in d:
            d[c] += 1
        else:
            d[c] = 1
    nums = [x for _,x in d.items()]
    nums.sort(reverse=True)
#    print(nums)
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

def mapHand(hand):
    m = {
        'A': '1',
        'K': '2',
        'Q': '3',
        'J': '4',
        'T': '5',
        '9': '6',
        '8': '7',
        '7': '8',
        '6': '9',
        '5': 'a',
        '4': 'b',
        '3': 'c',
        '2': 'd',
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

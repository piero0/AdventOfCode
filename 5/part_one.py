#!/bin/env python3

def create_ruleset(rules):
    d = {}
    for r in rules:
        a,b = r
        if not a in d:
            d[a] = {'l': set(), 'r': set() }
        d[a]['r'].add(b)
        if not b in d:
            d[b] = {'l': set(), 'r': set() }
        d[b]['l'].add(a)
    return d

def check_line(line, ruleset):
    for i in range(len(line)):
        l,r = set(line[:i]), set(line[i+1:])
        rl = ruleset[line[i]]['l']
        rr = ruleset[line[i]]['r']
        # print('n:', l, line[i], r)
        # print('r:', rl, rr)
        if not (l.issubset(rl) and r.issubset(rr)):
            return False
    return True

def main():
    with open('../data/2024/5/input') as f:
        data = f.readlines()

    read_rules = True
    rules = []
    lists = []
    for l in data:
        l = l.strip()
        if l == '':
            read_rules = False
            continue
        if read_rules:
            rules.append(l.split('|'))
        else:
            lists.append(l.split(','))
    ruleset = create_ruleset(rules)
    # print(rules)
    # print(lists)
    # print(ruleset)
    total = 0
    for l in lists:
        if check_line(l, ruleset):
            total += int(l[len(l)//2])

    print(total)

main()

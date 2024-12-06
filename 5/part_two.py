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

def create_edges(rules):
    d = {}
    for r in rules:
        a,b = r
        if a not in d:
            d[a] = []
        d[a].append(b)
    return d

def topo_sort(num, pres, order, indeg, edges):
    order.append(num)
    for e in edges[num]:
        if e in pres:
            indeg[e] -= 1
            if indeg[e] == 0:
                topo_sort(e, pres, order, indeg, edges)

    return order

def part2(line, edges):
    pres = set(line)
    #print(f'pres {pres}')
    indeg = {}
    start = []
    order = []
    for x in line:
        if x not in edges:
            continue
        for m in edges[x]:
            if m in pres:
                if m not in indeg:
                    indeg[m] = 0
                indeg[m]+=1
                #print(f'm {m} indeg {indeg[m]}')
    for x in line:
        if(x not in indeg or indeg[x] == 0):
            start.append(x)
    for x in start:
        topo_sort(x, pres, order, indeg, edges)
    return int(order[len(order)//2])


def check_line(line, ruleset):
    #print('line:', line)
    fail = False
    fails = []
    for i in range(len(line)):
        l,r = set(line[:i]), set(line[i+1:])
        rl = ruleset[line[i]]['l']
        rr = ruleset[line[i]]['r']
        # print('n:', l, line[i], r)
        # print('r:', rl, rr)
        if not (l.issubset(rl) and r.issubset(rr)):
            fails.append(line[i])
            fail = True
    if fail:
        #print(f'fails {fails}')
        pass
    return not fail

def main():
    filename = '../data/2024/5/test_input'
    #filename = '../data/2024/5/input'
    with open(filename) as f:
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
    edges = create_edges(rules)
    total = 0
    for l in lists:
        if check_line(l, ruleset):
            #total += int(l[len(l)//2])
            pass
        else:
            print(f'NOK: {l}')
            total += part2(l, edges)

    print(total)

main()

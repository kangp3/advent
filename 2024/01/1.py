#!/usr/bin/env python

ls = []
rs = []
with open('1.txt') as f:
    for row in f:
        if not row.split():
            continue
        print(row.split())
        l, r = row.split()
        l = int(l)
        r = int(r)
        ls.append(l)
        rs.append(r)

ls.sort()
rs.sort()
sum_dist = 0
for l, r in zip(ls, rs):
    dist = abs(r - l)
    print(l, r, dist)
    sum_dist += dist
print(sum_dist)

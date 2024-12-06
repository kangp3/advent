#!/usr/bin/env python
from collections import defaultdict

ls = []
rs = defaultdict(int)
with open('1.txt') as f:
    for row in f:
        if not row.split():
            continue
        print(row.split())
        l, r = row.split()
        l = int(l)
        r = int(r)
        ls.append(l)
        rs[r] += 1

similarity = 0
for l in ls:
    similarity += l * rs[l]
print(similarity)

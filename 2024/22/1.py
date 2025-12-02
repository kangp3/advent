#!/usr/bin/env python3
from tqdm import tqdm
import json
from collections import *
from copy import deepcopy
from functools import cmp_to_key
from functools import cache
from itertools import *
from util import *
import argparse
import graphlib
import math
import os
import re
import sys
import time


MODULO = 16777216


def main(test=False):
    nums = []
    with open("test.txt" if test else "input.txt") as f:
        for line in f:
            nums.append(int(line.strip()))

    def next_val(v):
        v = (v ^ (v * 64)) % MODULO
        v = (v ^ (v // 32)) % MODULO
        v = (v ^ (v * 2048)) % MODULO
        return v

    #cycles = []
    #visited = set()

    #for i in range(MODULO):
    #    if i in visited:
    #        continue
    #    start = i
    #    cycle = [i]
    #    i = next_val(i)
    #    while i != start:
    #        visited.add(i)
    #        cycle.append(i)
    #        i = next_val(i)
    #    cycles.append(cycle)

    #with open('cycle.json', 'w') as f:
    #    json.dump(cycles[1], f)

    with open('cycle.json') as f:
        cycle = json.load(f)

    diffs = []
    last_v = cycle[-1]
    for v in cycle:
        diffs.append(v%10 - last_v%10)
        last_v = v

    seqs = set()
    window = deque([
        diffs[-3],
        diffs[-2],
        diffs[-1],
        diffs[0],
    ])
    for diff in diffs:
        seqs.add(tuple(window))
        window.popleft()
        window.append(diff)
    #print(len(seqs))

    '''
    {
      2024: {
        (5, -4, -2, 1): 4,
        (-1, 0, 1, 2): 6,
        (1, 1, 1, 2): 8,
      },
    }

    {
      2024: (
        [2024, 9554439, 6855065, 897063, 12842024, ...],
        [None, 5, -4, -2, 1, ...],
      )
    }
    '''
    price_book = defaultdict(dict)
    for n in nums:
        window = deque([])

        last_v = None
        v = n
        for i in range(5):
            if last_v is not None:
                window.append(v%10 - last_v%10)

            last_v = v
            v = next_val(v)

        for i in range(2002 - 5):
            diff_seq = tuple(window)
            if diff_seq not in price_book[n]:
                price_book[n][diff_seq] = last_v % 10

            window.popleft()
            window.append(v%10 - last_v%10)

            last_v = v
            v = next_val(v)

    best_seq = None
    max_score = 0
    for seq in tqdm(seqs):
        score = 0
        for n in nums:
            price = price_book[n].get(seq)
            if price is not None:
                score += price
        if score > max_score:
            best_seq = seq
            max_score = score

    for seq in [(-2, 2, -1, 1)]:
        score = 0
        for n in nums:
            price = price_book[n].get(seq)
            if price is not None:
                print(n, price)
                score += price
        if score > max_score:
            best_seq = seq
            max_score = score

    # 1855 too low
    print(best_seq)
    print(max_score)

    return

    to_index = dict()
    for idx, i in enumerate(cycle):
        to_index[i] = idx

    res = 0
    seen_seqs = set()
    for n in nums:
        window = deque([])
        last = None
        diffs = deque([])
        for i in range(5):
            if last is None:
                pass

            window.append(n)
            last = n
            n = next_val(n)

        for i in range(2000 - 5):
            n = next_val(n)
        print(window)
        idx = to_index[n]
        idx + 3

    print(res)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

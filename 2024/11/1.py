#!/usr/bin/env python3
from collections import defaultdict
from copy import deepcopy
from functools import cmp_to_key
from itertools import product, combinations, permutations
from util import Grid
import argparse
import graphlib
import math
import os
import re
import sys
import time


class Node:
    def __init__(self, v):
        self.v = v
        self.next = []


def main(test=False):
    stones = []
    with open("test.txt" if test else "input.txt") as f:
        for line in f:
            stones = [int(v) for v in line.strip().split(' ')]

    edges = {}
    counts = defaultdict(int)
    for i in stones:
        counts[i] += 1
    for i in range(75):
        new_counts = defaultdict(int)
        for stone, count in counts.items():
            if stone in edges:
                new_edges = edges[stone]
            elif stone == 0:
                new_edges = [1]
            else:
                digs = int(math.log10(stone)) + 1
                if digs % 2 == 0:
                    ten_to = 10 ** (digs // 2)
                    new_edges = [stone // ten_to, stone % ten_to]
                else:
                    new_edges = [stone * 2024]
            for out in new_edges:
                new_counts[out] += count
        counts = new_counts

        s = 0
        for v in counts.values():
            s += v
        print(s)
    print(len(new_stones))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

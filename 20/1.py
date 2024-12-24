#!/usr/bin/env python3
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


def main(test=False):
    grid = []
    start = None
    end = None
    walls = set()
    with open("test.txt" if test else "input.txt") as f:
        for row_idx, line in enumerate(f):
            row = []
            for col_idx, c in enumerate(line):
                if c == 'S':
                    start = row_idx + col_idx*1j
                    c = '.'
                elif c == 'E':
                    end = row_idx + col_idx*1j
                    c = '.'
                elif c == '#':
                    walls.add(row_idx + col_idx*1j)
                row.append(c)
            grid.append(row)

    def y(coord):
        return int(coord.real)

    def x(coord):
        return int(coord.imag)

    def get_grid(grid, coord):
        return grid[y(coord)][x(coord)]


    cache = {end: 0}
    def walk(grid, start, end):
        visited = set()
        q = deque([(start, 0)])
        while q:
            curr, cheated, cheats, step, path, postcheat = q.popleft()
            if curr in path:
                continue
            if curr in cache:
                for idx, i in enumerate(reversed(postcheat)):
                    cache[i] = cache[curr] + idx
                # 9484
                step = step + cache[curr]
                if step != 9484:
                    print('ste', step)
                continue
            offs = [
                -1,
                1j,
                1,
                -1j,
            ]
            neighbors = [
                curr + off
                for off in offs
            ]
            for i in neighbors:
                if 0 <= y(i) < len(grid) and 0 <= x(i) < len(grid[0]):
                    if cheated and cheats > 1:
                        q.append((i, cheated, cheats-1, step+1, path | set([curr]), postcheat))
                    if cheated and cheats == 1:
                        if get_grid(grid, i) == '.':
                            q.append((i, cheated, cheats-1, step+1, path | set([curr]), postcheat))
                    if cheated and cheats == 0:
                        if get_grid(grid, i) == '.':
                            q.append((i, cheated, cheats, step+1, path | set([curr]), postcheat + [curr]))
                    if not cheated:
                        if get_grid(grid, i) == '.':
                            q.append((i, False, cheats, step+1, path | set([curr]), postcheat))
                        else:
                            q.append((i, True, cheats-1, step+1, path | set([curr]), postcheat))
        return -1

    orig = walk(grid, start, end)
    res = 0
    print(res)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

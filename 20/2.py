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
            line = line.strip()
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
    def walk(grid, start, end, cheat=20):
        visited = set()
        q = deque([(start, 0, [])])
        while q:
            curr, step, path = q.popleft()
            if curr in visited:
                continue
            visited.add(curr)
            if curr in cache:
                for idx, i in enumerate(reversed(path)):
                    cache[i] = idx + cache[curr] + 1
                return path + [curr]
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
                    if get_grid(grid, i) == '.':
                        q.append((i, step+1, path + [curr]))
        return -1

    orig = walk(grid, start, end, cheat=None)
    cheat = 2
    res = 0
    for step, node in enumerate(orig):
        for row_offset in range(-cheat, cheat+1):
            col_bounds = cheat-abs(row_offset)
            for col_offset in range(-col_bounds, col_bounds+1):
                cheat_offset = row_offset + col_offset * 1j
                i = node + cheat_offset
                if 0 <= y(i) < len(grid) and 0 <= x(i) < len(grid[0]):
                    if get_grid(grid, i) == '.':
                        if i not in cache:
                            print('cache miss')
                            walk(grid, i, end, cheat=None)
                        cost = cache[i] + step + abs(row_offset) + abs(col_offset)
                        if cost <= len(orig)-1-100:
                            print(node, cheat_offset, i)
                            res += 1

    for row_idx in range(len(grid)):
        printrow = []
        for col_idx in range(len(grid[0])):
            node = row_idx + col_idx * 1j
            if grid[row_idx][col_idx] == '#':
                printrow.append(' #')
            elif node in cache:
                printrow.append(f'{cache[node]:02}')
            else:
                printrow.append('.')
        print(' '.join(printrow))
    print(res)
    print(start)
    print(end)
    print(len(orig))
    #print(len(orig), [(n, cache[n]) for n in orig])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

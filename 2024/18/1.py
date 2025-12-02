#!/usr/bin/env python3
from collections import *
from copy import deepcopy
from functools import cmp_to_key
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
    if test:
        #nbytes = 12
        board_size = 7
    else:
        #nbytes = 1024
        board_size = 71

    def x(coord):
        return int(coord.imag)

    def y(coord):
        return int(coord.real)

    def get_grid(grid, coord):
        return grid[y(coord)][x(coord)]

    grid = [['.'] * board_size for i in range(board_size)]
    with open("test.txt" if test else "input.txt") as f:
        for idx, line in enumerate(f):
            print(idx)
            #if idx >= nbytes:
            #    break
            x2, y2 = [int(v) for v in line.strip().split(',')]
            grid[y2][x2] = '#'

            for row in grid:
                print(''.join(row))

            start = 0
            visited = set()
            q = deque([(start, 0, [start])])
            n_path = None
            n_steps = None
            while q:
                curr, steps, path = q.popleft()

                if curr in visited:
                    continue
                visited.add(curr)

                if curr == board_size-1 + (board_size-1) * 1j:
                    n_path = path
                    n_steps = steps
                    break

                neighbors = [
                    curr - 1,
                    curr + 1j,
                    curr + 1,
                    curr - 1j,
                ]
                for neighbor in neighbors:
                    if 0 <= x(neighbor) < board_size and 0 <= y(neighbor) < board_size:
                        #print(neighbor, get_grid(grid, neighbor))
                        if get_grid(grid, neighbor) == '.':
                            q.append((neighbor, steps+1, path+[neighbor]))
            if n_steps is None:
                print(idx)
                print((x2,y2))
                print(n_steps)
                break

                #for step in n_path:
                #    grid[y(step)][x(step)] = 'O'
            for row in grid:
                print(''.join(row))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

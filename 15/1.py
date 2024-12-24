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
    offsets = {
        '<': -1j,
        '^': -1,
        '>': 1j,
        'v': 1,
    }

    def coord(pos):
        return (int(pos.real), int(pos.imag))

    def grid_v(grid, pos):
        return grid[int(pos.real)][int(pos.imag)]

    grid = []
    moves = []
    pos = None
    is_moves = False
    with open("test.txt" if test else "input.txt") as f:
        for row_idx, line in enumerate(f):
            line = line.strip()
            if line == '':
                is_moves = True
                continue

            if not is_moves:
                row = []
                for col_idx, c in enumerate(line):
                    match c:
                        case '#':
                            row.append('#')
                            row.append('#')
                        case '.':
                            row.append(' ')
                            row.append(' ')
                        case 'O':
                            row.append('[')
                            row.append(']')
                        case '@':
                            row.append('@')
                            row.append(' ')
                            pos = complex(row_idx, col_idx*2)
                grid.append(row)
            else:
                for c in line:
                    moves.append(offsets[c])

    move_idx = 0
    for move in moves:
        printme = '\n'.join([''.join(row) for row in grid])
        print(printme + '\033[0;0H')
        sys.stdout.flush()
        time.sleep(0.05)

        next = pos + move
        if move in (-1j, 1j):
            while grid_v(grid, next) in ('[', ']'):
                next += move
            if grid_v(grid, next) == '#':
                continue
            while next != pos:
                next_c = coord(next)
                prev = next - move
                grid[next_c[0]][next_c[1]] = grid_v(grid, prev)
                next = prev
            next_c = coord(next)
            grid[next_c[0]][next_c[1]] = ' '
            pos = pos + move
        else:
            seen_boxes = set()
            boxes = []
            is_blocked = False
            d = deque([next])
            while d:
                curr = d.popleft()
                if grid_v(grid, curr) == '[':
                    d.append(curr + 1j + move)
                    d.append(curr + move)
                    if curr not in seen_boxes:
                        boxes.append(curr)
                        seen_boxes.add(curr)
                elif grid_v(grid, curr) == ']':
                    d.append(curr - 1j + move)
                    d.append(curr + move)
                    if curr - 1j not in seen_boxes:
                        boxes.append(curr - 1j)
                        seen_boxes.add(curr - 1j)
                elif grid_v(grid, curr) == '#':
                    is_blocked = True
                    break

            if is_blocked:
                continue

            for box in boxes[::-1]:
                next_c = coord(box + move)
                grid[next_c[0]][next_c[1]] = grid_v(grid, box)
                grid[next_c[0]][next_c[1]+1] = grid_v(grid, box + 1j)
                box_c = coord(box)
                grid[box_c[0]][box_c[1]] = ' '
                grid[box_c[0]][box_c[1]+1] = ' '

            next_c = coord(next)
            grid[next_c[0]][next_c[1]] = '@'
            pos_c = coord(pos)
            grid[pos_c[0]][pos_c[1]] = ' '
            pos = pos + move

        move_idx += 1


    res = 0
    for row_idx, row in enumerate(grid):
        for col_idx, v in enumerate(row):
            if v == '[':
                res += row_idx * 100 + col_idx
    print(res)



if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

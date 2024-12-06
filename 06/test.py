#!/usr/bin/env python3
import os
import sys
import time
from copy import deepcopy
import argparse
from collections import *
import re


def main(coords, test=False, is_logging_enabled=False):
    os.system('clear')

    grid = []
    with open("test.txt" if test else "input.txt") as f:
        for line in f:
            grid.append(list(line.strip()))
    grid[coords[0]][coords[1]] = "#"
    logging = deepcopy(grid)
    logging[coords[0]][coords[1]] = "\033[92;1m#\033[0m"

    def is_in_bounds(pos):
        return 0 <= pos[0] < len(grid) and 0 <= pos[1] < len(grid[0])
    
    off_idx = 0
    guard_pos = None
    for r_idx, row in enumerate(grid):
        for c_idx, v in enumerate(row):
            if v == '^':
                guard_pos = r_idx, c_idx
                logging[r_idx][c_idx] = "."
                break

    OFFSETS = [
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -1),
    ]
    OFF_LOGS = ["↑", "→", "↓", "←"]
    BIG_OFF_LOGS = ["\033[94;1m⬆\033[0m", "\033[94;1m⮕\033[0m", "\033[94;1m⬇\033[0m", "\033[94;1m⬅\033[0m"]
    BIG_OFF2_LOGS = ["\033[31;1m⬆\033[0m", "\033[31;1m⮕\033[0m", "\033[31;1m⬇\033[0m", "\033[31;1m⬅\033[0m"]
    CYCLE_LOG = "\033[31;1m꩜\033[0m"
    GUARD_LOG = "\033[93;1m⬤\033[0m"

    visited = set()
    last_pos = guard_pos
    while True:
        g_row, g_col = guard_pos

        if (guard_pos, off_idx) in visited:
            print("CYCLE!")
            break
        visited.add((guard_pos, off_idx))

        logging[last_pos[0]][last_pos[1]] = BIG_OFF_LOGS[off_idx]
        memory = logging[g_row][g_col]
        logging[g_row][g_col] = GUARD_LOG
        if is_logging_enabled:
            print("\033[0;0H")
            for row in logging:
                print(''.join(row))
            time.sleep(0.05)

        r_off, c_off = OFFSETS[off_idx]
        n_row = g_row + r_off
        n_col = g_col + c_off

        if n_row < 0 or n_row >= len(grid):
            break
        if n_col < 0 or n_col >= len(grid[0]):
            break

        if grid[g_row+r_off][g_col+c_off] in (".", '^'):
            guard_pos = (g_row+r_off, g_col+c_off)
        elif grid[g_row+r_off][g_col+c_off] == "#":
            if g_row+r_off == coords[0] and g_col+c_off == coords[1]:
                BIG_OFF_LOGS = BIG_OFF2_LOGS
            off_idx = (off_idx+1) % 4

        last_pos = guard_pos
        logging[g_row][g_col] = memory

    for row in logging:
        print(''.join(row))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("coords", type=lambda x: [int(v) for v in x.split(',')])
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    ap.add_argument("-l", "--logging", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(args.coords, test=args.test, is_logging_enabled=args.logging)

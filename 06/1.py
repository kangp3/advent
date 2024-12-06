#!/usr/bin/env python3
import os
import sys
import time
from copy import deepcopy
import argparse
from collections import *
import re


def main(test=False, is_logging_enabled=False):
    os.system('clear')

    grid = []
    with open("test.txt" if test else "input.txt") as f:
        for line in f:
            grid.append(list(line.strip()))
    logging = deepcopy(grid)

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
    CYCLE_LOG = "\033[31;1m꩜\033[0m"
    GUARD_LOG = "\033[93;1m⬤\033[0m"
    cycle_causers = defaultdict(set)

    # Explore backwards through the grid from the position and mark all positions
    # that would cause a cycle
    def baxtrapolate(pos, dir):
        q = deque([(pos, dir, 0)])
        curr_depth = 0
        while q:
            pos, dir, depth = q.popleft()

            r_pos, c_pos = pos
            r_off, c_off = OFFSETS[dir]

            if logging[r_pos][c_pos] == '.':
                logging[r_pos][c_pos] = OFF_LOGS[dir]
            if depth != curr_depth and is_logging_enabled:
                print("\033[0;0H")
                for row in logging:
                    print(''.join(row))
                #time.sleep(0.05)
                curr_depth = depth

            if dir in cycle_causers[pos]:
                continue
            cycle_causers[pos].add(dir)

            # If there's an obstacle to our left then backtrack from that obstacle!
            myleft_dir = (dir-1) % 4
            myleft_r_off, myleft_c_off = OFFSETS[myleft_dir]
            myleft_r_pos, myleft_c_pos = r_pos + myleft_r_off, c_pos + myleft_c_off
            if is_in_bounds((myleft_r_pos, myleft_c_pos)) and grid[myleft_r_pos][myleft_c_pos] == "#":
                q.append((pos, myleft_dir, depth+1))

            # Subtract, we're going backward!
            prev_r = r_pos - r_off
            prev_c = c_pos - c_off
            if is_in_bounds((prev_r, prev_c)) and grid[prev_r][prev_c] != "#":
                q.append(((prev_r, prev_c), dir, depth+1))

    visited = set()
    last_pos = guard_pos
    cycle_count = 0
    while True:
        g_row, g_col = guard_pos
        visited.add((g_row, g_col))

        logging[last_pos[0]][last_pos[1]] = BIG_OFF_LOGS[off_idx]
        memory = logging[g_row][g_col]
        logging[g_row][g_col] = GUARD_LOG
        if is_logging_enabled:
            print("\033[0;0H")
            for row in logging:
                print(''.join(row))
            #time.sleep(0.05)

        baxtrapolate(guard_pos, off_idx)
        found_cycle = False
        if (g_row, g_col) in cycle_causers:
            seen_offsets = cycle_causers[(g_row, g_col)]
            if (off_idx+1) % 4 in seen_offsets:
                obs_coords = (g_row + OFFSETS[off_idx][0], g_col + OFFSETS[off_idx][1])
                if obs_coords not in visited:
                    print("CYCLE:", obs_coords)
                    if obs_coords == (100, 64):
                        break
                    found_cycle = True
                    cycle_count += 1

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
            off_idx = (off_idx+1) % 4

        last_pos = guard_pos
        logging[g_row][g_col] = CYCLE_LOG if found_cycle else memory

    for row in logging:
        print(''.join(row))
    print(cycle_count)
    #print(square_count)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    ap.add_argument("-l", "--logging", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test, is_logging_enabled=args.logging)

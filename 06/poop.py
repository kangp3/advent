#!/usr/bin/env python3
from copy import deepcopy
import argparse
from collections import *
import re


def main(test=False):
    orig_grid = []
    with open("test.txt" if test else "input.txt") as f:
        for line in f:
            orig_grid.append(list(line.strip()))
    
    cycle_count = 0
    for ob_row in range(len(orig_grid)):
        for ob_col in range(len(orig_grid[0])):
            grid = deepcopy(orig_grid)
            if grid[ob_row][ob_col] != '.':
                continue
            grid[ob_row][ob_col] = "#"

            r_off = -1
            c_off = 0
            guard_pos = None
            for r_idx, row in enumerate(grid):
                for c_idx, v in enumerate(row):
                    if v == '^':
                        guard_pos = r_idx, c_idx
                        break

            visited = set()
            count = 0
            is_cycle = False
            while True:
                #print(guard_pos, r_off, c_off)
                g_row, g_col = guard_pos
                if (g_row, g_col, r_off, c_off) in visited:
                    print("CYCLE:", (ob_row, ob_col), (g_row, g_col, r_off, c_off))
                    is_cycle = True
                    break
                visited.add((g_row, g_col, r_off, c_off))
                n_row = g_row + r_off
                n_col = g_col + c_off

                if n_row < 0 or n_row >= len(grid):
                    break
                if n_col < 0 or n_col >= len(grid[0]):
                    break

                if grid[g_row+r_off][g_col+c_off] in (".", '^'):
                    guard_pos = (g_row+r_off, g_col+c_off)
                elif grid[g_row+r_off][g_col+c_off] == "#":
                    guard_off = (r_off, c_off)
                    if guard_off == (-1, 0):
                        r_off = 0
                        c_off = 1
                    elif guard_off == (0, 1):
                        r_off = 1
                        c_off = 0
                    elif guard_off == (1, 0):
                        r_off = 0
                        c_off = -1
                    elif guard_off == (0, -1):
                        r_off = -1
                        c_off = 0

                    #print(g_row, last_pos[0], g_col, last_pos[1])
                    #last_len = abs(g_row - last_pos[0]) + abs(g_col - last_pos[1])
                    #if last_1 is None:
                    #    last_1 = last_len
                    #    last_pos = guard_pos
                    #elif last_2 is None:
                    #    last_2 = last_1
                    #    last_1 = last_len
                    #    last_pos = guard_pos
                    #elif last_3 is None:
                    #    last_3 = last_2
                    #    last_2 = last_1
                    #    last_1 = last_len
                    #    last_pos = guard_pos
                    #else:
                    #    print(f'({g_row}, {g_col})', last_3, last_2, last_1, last_len)
                    #    if last_len >= last_2 and last_3 >= last_1:
                    #        print("YES")
                    #        square_count += 1
                    #    last_3 = last_2
                    #    last_2 = last_1
                    #    last_1 = last_len
                    #    last_pos = guard_pos

                        #rcoord_counts = defaultdict(int)
                        #ccoord_counts = defaultdict(int)
                        #is_square = True
                        #is_r_match = None
                        #last_r = last_3[0]
                        #last_c = last_3[1]
                        #print(last_3, last_2, last_1)
                        #for r, c in (last_2, last_1):
                        #    if last_r == r:
                        #        if is_r_match is None:
                        #            is_r_match = True
                        #        elif is_r_match:
                        #            is_square = False
                        #            break
                        #    elif last_c == c:
                        #        if is_r_match is None:
                        #            is_r_match = False
                        #        elif not is_r_match:
                        #            is_square = False
                        #            break
                        #    rcoord_counts[r] += 1
                        #    ccoord_counts[c] += 1
                        #if is_square:
                        #    square_count += 1

                #square_count += 1
                #if count >= 55:
                #    break
            if is_cycle:
                cycle_count += 1

    print(cycle_count)
    #print(square_count)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

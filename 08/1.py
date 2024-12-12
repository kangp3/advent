#!/usr/bin/env python3
import math
import argparse
from itertools import *
from collections import *
import re


def main(test=False):
    grid = []
    nodes = defaultdict(list)
    with open("test.txt" if test else "input.txt") as f:
        for row_idx, line in enumerate(f):
            row = []
            for col_idx, c in enumerate(line.strip()):
                if c != '.':
                    nodes[c].append((row_idx, col_idx))
                row.append(c)
            grid.append(row)

    print(len(grid), len(grid[0]))
    def is_in_bounds(row, col):
        return 0 <= row < len(grid) and 0 <= col < len(grid[0])

    antinodes = set()
    for node, coords in nodes.items():
        print(node)
        for v1, v2 in permutations(coords, r=2):
            r_diff_orig = abs(v1[0] - v2[0])
            c_diff_orig = abs(v1[1] - v2[1])
            r_diff = r_diff_orig // math.gcd(r_diff_orig, c_diff_orig)
            c_diff = c_diff_orig // math.gcd(r_diff_orig, c_diff_orig)
            print("GCD", math.gcd(r_diff_orig, c_diff_orig), r_diff, c_diff)
            curr_pos = [v1[0], v1[1]]
            while is_in_bounds(*curr_pos):
                antinodes.add(tuple(curr_pos))
                if v1[0] <= v2[0]:
                    curr_pos[0] -= r_diff
                else:
                    curr_pos[0] += r_diff
                if v1[1] <= v2[1]:
                    curr_pos[1] -= c_diff
                else:
                    curr_pos[1] += c_diff
            curr_pos = [v1[0], v1[1]]
            while is_in_bounds(*curr_pos):
                antinodes.add(tuple(curr_pos))
                if v1[0] <= v2[0]:
                    curr_pos[0] += r_diff
                else:
                    curr_pos[0] -= r_diff
                if v1[1] <= v2[1]:
                    curr_pos[1] += c_diff
                else:
                    curr_pos[1] -= c_diff
    print(sorted(antinodes))
    print(len(antinodes))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

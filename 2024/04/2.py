#!/usr/bin/env python3
import argparse
from collections import *
import re


def main(test=False):
    print(test)
    grid = []
    with open("test.txt" if test else "input.txt") as f:
        for line in f:
            grid.append(line.strip())

    count = 0
    for row_idx in range(1, len(grid)-1):
        row = grid[row_idx]
        for col_idx in range(1, len(row)-1):
            if grid[row_idx][col_idx] == 'A':
                up_left = grid[row_idx-1][col_idx-1]
                up_right = grid[row_idx-1][col_idx+1]
                down_left = grid[row_idx+1][col_idx-1]
                down_right = grid[row_idx+1][col_idx+1]
                if (up_left, down_right) in [('M', 'S'), ('S', 'M')] and (up_right, down_left) in [('M', 'S'), ('S', 'M')]:
                    count += 1
    print(count)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

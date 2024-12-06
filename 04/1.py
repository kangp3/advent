#!/usr/bin/env python3
import argparse
from collections import *
import re


def main(test=False):
    grid = []
    with open("test.txt" if test else "input.txt") as f:
        for line in f:
            grid.append(line.strip())

    count = 0
    for row_idx, row in enumerate(grid):
        count += len(list(re.finditer(r'XMAS', row)))
        count += len(list(re.finditer(r'SAMX', row)))

    grid_cols = [[] for col in grid[0]]
    for row in grid:
        for col_idx, let in enumerate(row):
            grid_cols[col_idx].append(let)
        #for line in grid_cols:
        #    print(''.join(line))
    for row_idx, row in enumerate(grid_cols):
        count += len(list(re.finditer(r'XMAS', ''.join(row))))
        count += len(list(re.finditer(r'SAMX', ''.join(row))))

    diag_cols = [[] for i in range(len(grid[0]) + len(grid[0]))]
    for col_idx in range(-len(grid[0]), len(grid[0])):
        for row_idx in range(max(col_idx, 0), min(col_idx + len(grid[0]), len(grid[0]))):
            if col_idx < 0:
                diag_cols[col_idx+len(grid[0])].append(grid[row_idx-col_idx][row_idx])
            else:
                diag_cols[col_idx+len(grid[0])].append(grid[row_idx-col_idx][row_idx])
        #for line in diag_cols:
        #    print(''.join(line))
    for row_idx, row in enumerate(diag_cols):
        count += len(list(re.finditer(r'XMAS', ''.join(row))))
        count += len(list(re.finditer(r'SAMX', ''.join(row))))

    diag2_cols = [[] for i in range(len(grid[0]) + len(grid[0]))]
    for col_idx in range(-len(grid[0]), len(grid[0])):
        for row_idx in range(max(col_idx, 0), min(col_idx + len(grid[0]), len(grid[0]))):
            if col_idx < 0:
                diag2_cols[col_idx+len(grid[0])].append(grid[-col_idx+row_idx][len(grid[0])-row_idx-1])
            else:
                diag2_cols[col_idx+len(grid[0])].append(grid[row_idx-col_idx][len(grid[0])-row_idx-1])
        #for line in diag2_cols:
        #    print(''.join(line))
    for row_idx, row in enumerate(diag2_cols):
        count += len(list(re.finditer(r'XMAS', ''.join(row))))
        count += len(list(re.finditer(r'SAMX', ''.join(row))))

    print(grid)
    print(count)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

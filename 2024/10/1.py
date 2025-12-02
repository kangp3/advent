#!/usr/bin/env python3
import argparse
from util import Grid
from collections import *
import re


def main(test=False):
    grid = Grid.from_file("test.txt" if test else "input.txt", type=int)

    starts = []
    for row_idx, row in enumerate(grid):
        for col_idx, v in enumerate(row):
            if v == 0:
                starts.append(grid.coord(complex(row_idx, col_idx)))

    sum_all = 0
    for start in starts:
        st = [start]
        visited = set()
        score = 0
        while st:
            curr = st.pop()

            if curr in visited:
                continue
            visited.add(curr)

            if grid[curr.row][curr.col] == 9:
                score += 1
                sum_all += 1

            for neighbor in curr.neighbors():
                if grid[neighbor.row][neighbor.col] == grid[curr.row][curr.col] + 1:
                    st.append(neighbor)
    print(sum_all)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

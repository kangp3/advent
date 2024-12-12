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
    grid = Grid.from_file("test.txt" if test else "input.txt")
    visited = set()
    res = 0
    for row_idx, row in enumerate(grid):
        for col_idx, v in enumerate(row):
            if grid.coord(complex(row_idx, col_idx)) in visited:
                continue

            perimeter = 0
            area = 0
            q = deque([grid.coord(complex(row_idx, col_idx))])
            while q:
                curr = q.popleft()

                if curr in visited:
                    continue
                visited.add(curr)

                neighbors = [n for n in curr.neighbors() if grid[n.row][n.col] == v]
                perimeter += 4 - len(neighbors)
                area += 1
                for n in neighbors:
                    q.append(n)

            res += perimeter * area
                
    print(res)



if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

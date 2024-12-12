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

    extended = grid.copy()
    for row in extended:
        row.extend(['.'] * len(row))
    for i in range(len(extended.grid)):
        extended.grid.append(['.'] * len(extended[0]))

    visited = set()
    res = 0
    for row_idx, row in enumerate(grid):
        for col_idx, v in enumerate(row):
            if grid.coord(complex(row_idx, col_idx)) in visited:
                continue

            edge_nodes = set()
            edges = defaultdict(set)
            area = 0
            q = deque([grid.coord(complex(row_idx, col_idx))])
            while q:
                curr = q.popleft()

                if curr in visited:
                    continue
                visited.add(curr)

                neighbors = set([n for n in curr.neighbors() if grid[n.row][n.col] == v])
                ext_coords = extended.coord(curr.coords * 2)
                if curr.offset(-1) not in neighbors:
                    c1 = ext_coords
                    c2 = ext_coords.offset(1j)
                    edge_nodes.add(c1)
                    edge_nodes.add(c2)
                    edges[c1].add(c2)
                    edges[c2].add(c1)
                else:
                    c1 = ext_coords
                    c2 = ext_coords.offset(-1)
                    edges[c1].add(c2)
                    edges[c2].add(c1)
                    edge_nodes.add(c1)
                    edge_nodes.add(c2)
                    c1 = ext_coords.offset(1j)
                    c2 = ext_coords.offset(-1+1j)
                    edges[c1].add(c2)
                    edges[c2].add(c1)
                    edge_nodes.add(c1)
                    edge_nodes.add(c2)
                if curr.offset(1j) not in neighbors:
                    c1 = ext_coords.offset(1j)
                    c2 = ext_coords.offset(1+1j)
                    edge_nodes.add(c1)
                    edge_nodes.add(c2)
                    edges[c1].add(c2)
                    edges[c2].add(c1)
                else:
                    c1 = ext_coords.offset(1j)
                    c2 = ext_coords.offset(2j)
                    edges[c1].add(c2)
                    edges[c2].add(c1)
                    edge_nodes.add(c1)
                    edge_nodes.add(c2)
                    c1 = ext_coords.offset(1+1j)
                    c2 = ext_coords.offset(1+2j)
                    edges[c1].add(c2)
                    edges[c2].add(c1)
                    edge_nodes.add(c1)
                    edge_nodes.add(c2)
                if curr.offset(1) not in neighbors:
                    c1 = ext_coords.offset(1+1j)
                    c2 = ext_coords.offset(1)
                    edge_nodes.add(c1)
                    edge_nodes.add(c2)
                    edges[c1].add(c2)
                    edges[c2].add(c1)
                else:
                    c1 = ext_coords.offset(1+1j)
                    c2 = ext_coords.offset(2+1j)
                    edges[c1].add(c2)
                    edges[c2].add(c1)
                    edge_nodes.add(c1)
                    edge_nodes.add(c2)
                    c1 = ext_coords.offset(1)
                    c2 = ext_coords.offset(2)
                    edges[c1].add(c2)
                    edges[c2].add(c1)
                    edge_nodes.add(c1)
                    edge_nodes.add(c2)
                if curr.offset(-1j) not in neighbors:
                    c1 = ext_coords
                    c2 = ext_coords.offset(1)
                    edge_nodes.add(c1)
                    edge_nodes.add(c2)
                    edges[c1].add(c2)
                    edges[c2].add(c1)
                else:
                    c1 = ext_coords
                    c2 = ext_coords.offset(-1j)
                    edges[c1].add(c2)
                    edges[c2].add(c1)
                    edge_nodes.add(c1)
                    edge_nodes.add(c2)
                    c1 = ext_coords.offset(1)
                    c2 = ext_coords.offset(1-1j)
                    edges[c1].add(c2)
                    edges[c2].add(c1)
                    edge_nodes.add(c1)
                    edge_nodes.add(c2)
                    
                area += 1
                for n in neighbors:
                    q.append(n)

            squares = set()
            for e_n in edge_nodes:
                if e_n.row % 2 == 0 or e_n.col % 2 == 0:
                    continue
                if (
                    e_n.offset(1j) in edge_nodes and
                    e_n.offset(1+1j) in edge_nodes and
                    e_n.offset(1) in edge_nodes
                ):
                    squares.add(e_n)
                    squares.add(e_n.offset(1j))
                    squares.add(e_n.offset(1+1j))
                    squares.add(e_n.offset(1))
            edge_nodes = edge_nodes - squares

            #print([(n.coords, n.row, n.col) for n in edge_nodes])
            all_sides = 0
            while edge_nodes:
                start = min(edge_nodes, key=lambda x: (x.row, x.col))
                #print(start.coords)
                curr = start
                visited2 = set()
                off = 1
                sides = 0
                while curr != start or sides == 0:
                    #print(' ', curr.coords, [n.coords for n in edges[curr]])
                    last = None
                    visited2.add(curr)
                    while curr.offset(off) in edges[curr]:
                        last = curr
                        curr = curr.offset(off)
                        visited2.add(curr)
                    #print("NS", curr.coords, [n.coords for n in edges[curr]])
                    neighbors = [n for n in edges[curr] if n != last]
                    #print(curr.coords, off, [n.coords for n in neighbors])
                    next_edge = None
                    for n in neighbors:
                        #print(' ', n.coords)
                        if curr.coords - n.coords != off:
                            next_edge = n
                        if n == start:
                            break
                    if next_edge is None:
                        sides += 1
                        break
                    off = next_edge.coords - curr.coords
                    sides += 1
                all_sides += sides
                edge_nodes = edge_nodes - visited2
            print(v, area, all_sides)
            res += all_sides * area
                
    print(res)



if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

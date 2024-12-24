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
from heapq import *


def main(test=False):
    grid = []
    orig_start = None
    end = None
    with open("test.txt" if test else "input.txt") as f:
        for row_idx, line in enumerate(f):
            row = []
            for col_idx, v in enumerate(line):
                if v == 'E':
                    end = complex(row_idx, col_idx)
                elif v == 'S':
                    orig_start = complex(row_idx, col_idx)
                row.append(v)
            grid.append(row)
    print(orig_start)
    print(end)
    for line in grid:
        print(''.join(line))


    def inbounds(grid, coords):
        return 0 <= int(coords.real) < len(grid) and 0 <= int(coords.imag) < len(grid[0])

    def get_grid(grid, coords):
        return grid[int(coords.real)][int(coords.imag)]

    def to_coords(cplx):
        return (int(cplx.real), int(cplx.imag))

    def from_coords(coords):
        return complex(*coords)

    OFFSETS = [
        1j,
        -1,
        -1j,
        1,
    ]

    visited = set()
    edges = defaultdict(set)
    costs = {}
    q = [(0, (to_coords(orig_start), 0), set())]
    reses = []
    final_cost = None
    while q:
        cost, place, path = heappop(q)
        pos, off_idx = place
        pos = from_coords(pos)
        print('s', cost, pos, off_idx, [to_coords(pos)])
        if (pos, off_idx) in path or get_grid(grid, pos) == '#':
            continue
        visited.add((pos, off_idx))
        if get_grid(grid, pos) == 'E':
            if final_cost is None or cost == final_cost:
                final_cost = cost
                #print('E??', pos)
                reses.append((cost, path))
            if final_cost is not None and cost > final_cost:
                break

        neighbors = [
            (pos + OFFSETS[off_idx], off_idx, 1),
            (pos, (off_idx-1) % 4, 1000),
            (pos, (off_idx+1) % 4, 1000),
        ]
        for npos, noff_idx, ncost in neighbors:
            curr_cost = costs.get((npos, noff_idx), float('inf'))
            new_cost = cost + ncost
            #print(" ", (npos, noff_idx), curr_cost, new_cost)
            if new_cost <= curr_cost:
                costs[(npos, noff_idx)] = new_cost
                #print("    PUSHING", (npos, noff_idx))
                heappush(q, (new_cost, (to_coords(npos), noff_idx), path | set([to_coords(npos)])))
        '''
        curr = pos
        dist = 0
        dirxn = OFFSETS[off_idx]
        grid_v = get_grid(grid, curr)
        while grid_v != '#':
            print(' ', curr, dirxn)
            if grid_v == 'E':
                curr_cost = costs.get((curr, off_idx), float('inf'))
                new_cost = cost + dist
                print('   ', curr_cost, new_cost)
                if new_cost < curr_cost:
                    costs[(curr, off_idx)] = new_cost
                    heappush(q, (new_cost, (curr, off_idx), path))
            if curr + OFFSETS[(off_idx-1)%4] != '#':
                curr_cost = costs.get((curr, (off_idx-1)%4), float('inf'))
                new_cost = cost + dist + 1000
                print('   ', curr_cost, new_cost)
                if new_cost < curr_cost:
                    costs[curr] = new_cost
                    heappush(q, (new_cost, (curr, (off_idx-1) % 4), path))
            if curr + OFFSETS[(off_idx+1)%4] != '#':
                curr_cost = costs.get((curr, (off_idx+1)%4), float('inf'))
                new_cost = cost + dist + 1000
                print('   ', curr_cost, new_cost)
                if new_cost < curr_cost:
                    costs[curr] = new_cost
                    heappush(q, (new_cost, (curr, (off_idx+1) % 4), path))

            dist += 1
            curr += dirxn
            grid_v = get_grid(grid, curr)
        '''
    nodes = set()
    for _, path in reses:
        for node in path:
            ridx, cidx = node
            grid[ridx][cidx] = 'O'
            nodes.add(node)
    for line in grid:
        print(''.join(line))
    print(len(reses), reses)
    print(len(nodes))
    return

    '''
        curr = pos
        neighbors = []
        dist = 0
        grid_v = get_grid(grid, curr)
        while grid_v != '#':
            if grid_v == 'E':
                edges[(curr, pos)].add((curr, off_idx, dist))
            if curr + OFFSETS[(off_idx-1)%4] != '#':
                edges[(curr, pos)].add((curr, (off_idx-1) % 4, 1000 + dist))
            if curr + OFFSETS[(off_idx+1)%4] != '#':
                edges[(curr, pos)].add((curr, (off_idx+1) % 4, 1000 + dist))
            dist += 1
            curr = pos + dirxn
            grid_v = get_grid(grid, curr + dirxn)
    off_idx = 0
    def find_path(start, off_idx, end, visited):
        print('S', start, off_idx)
        if start == end:
            return [0]
        dirxn = OFFSETS[off_idx]
        scores = []

        nvisited = set(visited)
        nvisited.add(start)
        neighbors = [
            (start + dirxn, off_idx, 1),
            (start + OFFSETS[(off_idx - 1) % 4], (off_idx - 1) % 4, 1001),
            (start + OFFSETS[(off_idx + 1) % 4], (off_idx + 1) % 4, 1001),
        ]
        for pos, ndirxn, cost in neighbors:
            print("  N", pos, ndirxn, cost, inbounds(grid, pos), get_grid(grid, pos), pos not in visited)
            if inbounds(grid, pos) and get_grid(grid, pos) in ('.', 'E') and pos not in nvisited:
                print('  doing')
                scores.extend([s + cost for s in find_path(pos, ndirxn, end, nvisited)])
                print(' ', start, scores)
        if start == orig_start:
            return min(scores)
        else:
            return scores

    print(find_path(orig_start, 0, end, set()))
    '''


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

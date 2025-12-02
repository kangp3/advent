#!/usr/bin/env python3
from collections import *
import graphviz
from copy import deepcopy
from functools import cmp_to_key
from functools import cache
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
    nodes = set()
    edges = defaultdict(set)
    with open("test.txt" if test else "input.txt") as f:
        for line in f:
            f, t = line.strip().split('-')
            edges[f].add(t)
            edges[t].add(f)
            nodes.add(f)
            nodes.add(t)

    #dot = graphviz.Graph('aoc-poop', comment='Advent Poop', engine='sfdp')
    #dot.attr(size='1800,1500')
    #dot.attr(nodesep='100')
    #for node in nodes:
    #    dot.node(node, node)

    #visited = set()
    #for f, ts in edges.items():
    #    for t in ts:
    #        if (f, t) in visited or (t, f) in visited:
    #            continue
    #        visited.add((f, t))
    #        dot.edge(f, t, constraint='false')

    #dot = dot.unflatten(stagger=3)

    #dot.view()
    #return

    #dot.render(directory='advent-poop-viz', view=True)  

    #return

    def find_largest_party(candidates, party):
        if len(candidates) > 400:
            print(len(candidates), len(nodes))
        largest_party = party
        for idx, c in enumerate(candidates):
            if not all(c in edges[nbr] for nbr in party):
                continue
            n_party = find_largest_party(candidates[idx+1:], party | set([c]))
            if len(n_party) > len(largest_party):
                largest_party = n_party
        return largest_party

    all_parties = find_largest_party(list(nodes), set())
    print(','.join(sorted(all_parties)))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

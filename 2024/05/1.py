#!/usr/bin/env python3
import argparse
from collections import *
from functools import cmp_to_key
import graphlib
import re


def main(test=False):
    with open("test.txt" if test else "input.txt") as f:
        done_ingesting = False
        edges = defaultdict(set)
        orders = []
        for line in f:
            if line == '\n':
                done_ingesting = True
            elif not done_ingesting:
                left_right = line.strip().split('|')
                left = left_right[0]
                right = left_right[1]
                edges[left].add(right)
            else:
                line = line.strip().split(',')
                print(''.join([chr(int(c)) for c in line]))
                orders.append(line)

        res = 0
        def compare(item1, item2):
            if item2 in edges[item1]:
                return -1
            if item1 in edges[item2]:
                return 1
            return 0
        for order in orders:
            is_valid = True
            for idx, v in enumerate(order):
                for v2 in order[idx+1:]:
                    if v2 not in edges[v]:
                        is_valid = False
                        break
                if not is_valid:
                    break
            if not is_valid:
                print(order)
                srt = sorted(order, key=cmp_to_key(compare))
                print(srt)
                res += int(srt[len(order) // 2])
        print(res)

        #ts = graphlib.TopologicalSorter(edges)
        #print(list(ts.static_order()))
        #print(edges['44'])
        #print(orders)



if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

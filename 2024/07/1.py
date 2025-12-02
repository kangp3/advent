#!/usr/bin/env python3
import argparse
import math
from collections import *
import re
from itertools import *


def main(test=False):
    eqs = dict()
    with open("test.txt" if test else "input.txt") as f:
        for line in f:
            stuff = line.strip().split(':')
            eqs[int(stuff[0])] = [int(v) for v in stuff[1].strip().split(' ')]

    def solve_eq(target, vals):
        for ops in product('+*|', repeat=len(vals)-1):
            res = vals[0]
            for op, val in zip(ops, vals[1:]):
                if op == "+":
                    res += val
                elif op == "*":
                    res *= val
                elif op == "|":
                    digs = math.floor(math.log10(val)) + 1
                    res = res * 10**digs + val
            if res == target:
                return True
        return False

    res = 0
    for target, vals in eqs.items():
        if solve_eq(target, vals):
            res += target
    print(res)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

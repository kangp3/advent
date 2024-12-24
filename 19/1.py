#!/usr/bin/env python3
from functools import cache
import argparse


def main(test=False):
    parts = []
    designs = []

    is_designs = False
    with open("test.txt" if test else "input.txt") as f:
        for line in f:
            line = line.strip()
            if not line:
                is_designs = True
                continue

            if is_designs:
                designs.append(line)
            else:
                parts = line.split(', ')

    #@cache
    def solve(design):
        if design == '':
            return 1
        ways = 0
        for part in parts:
            if design.startswith(part):
                print(design, part)
                if solve(design[len(part):]):
                    return True
        return ways

    res = 0
    for design in designs:
        print(design)
        ways = solve(design)
        print(design, ways)
        res += ways
    print(res)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

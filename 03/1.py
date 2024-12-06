#!/usr/bin/env python3
import argparse
from collections import *
import re


def main(test=False):
    res = 0
    is_enabled = True
    with open("test.txt" if test else "input.txt") as f:
        for line in f:
            for args in re.finditer(r"mul\((\d+),(\d+)\)|don't\(\)|do\(\)", line):
                if args[0].startswith("don't"):
                    is_enabled = False
                elif args[0].startswith("do"):
                    is_enabled = True
                elif is_enabled:
                    res += int(args[1]) * int(args[2])
    print(res)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

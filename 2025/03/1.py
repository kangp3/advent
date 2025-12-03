#!/usr/bin/env python3
from collections import *
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
    with open("test.txt" if test else "input.txt") as f:
        banks = [
            [
                int(c)
                for c in
                line.strip()
            ]
            for line in f
        ]

    res = 0
    for bank in banks:
        max_l = 0
        max_r = 0
        for dig in bank[:-1]:
            if dig > max_l:
                max_l = dig
                max_r = 0
                continue
            if dig > max_r:
                max_r = dig
        if bank[-1] > max_r:
            max_r = bank[-1]
        joltage = 10 * max_l + max_r
        res += joltage
    print(res)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

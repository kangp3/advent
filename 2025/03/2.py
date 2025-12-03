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


#MAX_DIGS = 2
MAX_DIGS = 12


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
        max_digs = [0] * MAX_DIGS
        for bank_idx, dig in enumerate(bank):
            remaining_idx = max(MAX_DIGS - (len(bank) - bank_idx), 0)
            for idx in range(remaining_idx, MAX_DIGS):
                if dig > max_digs[idx]:
                    max_digs[idx] = dig
                    for j in range(idx+1, MAX_DIGS):
                        max_digs[j] = 0
                    break

        joltage = 0
        for dig in max_digs:
            joltage *= 10
            joltage += dig

        res += joltage

    print(res)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

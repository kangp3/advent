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
    pos = 50
    turns = []
    with open("test.txt" if test else "input.txt") as f:
        for line in f:
            turn = 1
            if line[0] == "L":
                turn = -1
            turn *= int(line[1:-1])
            turns.append(turn)

    res = 0
    for turn in turns:
        if turn == 0:
            continue
        pos = pos % 100

        print(pos, res)
        if pos + turn <= 0:
            if pos != 0:
                res += 1
            turn += pos
            pos = 0
        elif pos + turn >= 100:
            res += 1
            turn -= (100 - pos)
            pos = 0

        res += abs(turn) // 100
        pos += turn % 100

    print(res)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

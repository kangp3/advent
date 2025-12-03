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
    ranges = []
    with open("test.txt" if test else "input.txt") as f:
        for line in f:
            for range_str in line.strip().split(','):
                ranges.append([int(x) for x in range_str.split('-')])

    res = 0
    for low, high in ranges:
        for i in range(low, high+1):
            as_str = str(i)
            strlen = len(as_str)
            if strlen % 2 == 1:
                continue
            
            if as_str[:strlen//2] == as_str[strlen//2:]:
                res += i
    print(res)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

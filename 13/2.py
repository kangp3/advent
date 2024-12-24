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


def main(test=False):
    puzzles = []
    with open("test.txt" if test else "input.txt") as f:
        btn_a = None
        btn_b = None
        prize = None
        for line in f:
            if not line.strip():
                continue
            key, val = line.strip().split(':')
            match key:
                case 'Button A':
                    btn_a = tuple([float(v.strip()[1:]) for v in val.split(',')])
                case 'Button B':
                    btn_b = tuple([float(v.strip()[1:]) for v in val.split(',')])
                case 'Prize':
                    prize = tuple([10000000000000.+float(v.strip()[2:]) for v in val.split(',')])
                    #prize = tuple([float(v.strip()[2:]) for v in val.split(',')])
                    puzzles.append((btn_a, btn_b, prize))
    
    def close_enough(a):
        return abs(int(a) - a) < 1e-6

    def solve_puzzle(puzzle):
        btn_a, btn_b, prize = puzzle

        scaling = btn_b[0]/btn_b[1]
        numerator = prize[0] - scaling * prize[1]
        denominator = btn_a[0] - scaling * btn_a[1]
        a_presses = round(numerator / denominator)
        b_presses = round((prize[0] - a_presses * btn_a[0]) / btn_b[0])

        print(' ', (a_presses * btn_a[0] + b_presses * btn_b[0], a_presses * btn_a[1] + b_presses * btn_b[1]), prize)
        if (a_presses * btn_a[0] + b_presses * btn_b[0], a_presses * btn_a[1] + b_presses * btn_b[1]) == prize:
            return a_presses * 3 + b_presses
        return None


        #def get_moves(remaining):
        #    x, y = remaining
        #    #print(x, y)
        #    if x < 0 or y < 0:
        #        return None
        #    elif x == 0 and y == 0:
        #        return 0

        #    a = get_moves((remaining[0] - btn_a[0], remaining[1] - btn_a[1]))
        #    b = get_moves((remaining[0] - btn_b[0], remaining[1] - btn_b[1]))
        #    #print(remaining, a, b)
        #    if a is None and b is None:
        #        return None
        #    if a is None:
        #        return b + 1
        #    if b is None:
        #        return a + 3
        #    return min(a+3, b+1)

        #return get_moves(prize)

    res = 0
    for puzzle in puzzles:
        print(puzzle)
        soln = solve_puzzle(puzzle)
        if soln is None:
            continue
        res += soln
    print(res)

    # 56057898015375 too low
    # 70420658929195 too low
    # 70841168090711 too low


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

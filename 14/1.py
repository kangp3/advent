#!/usr/bin/env python3
from collections import *
from copy import deepcopy
from functools import cmp_to_key
from itertools import *
from matplotlib import pyplot as plt
from util import *
import argparse
import graphlib
import math
import os
import re
import sys
import time


def main(test=False):
    dims = (11, 7) if test else (101, 103)
    robots = []
    with open("test.txt" if test else "input.txt") as f:
        for line in f:
            ps, vs = line.strip().split(' ')
            p = tuple([int(x) for x in ps.split('=')[1].split(',')])
            v = tuple([int(x) for x in vs.split('=')[1].split(',')])
            robots.append([complex(*p), complex(*v)])

    i = 0
    a = ''
    reses = []
    for i in range(6398):
        grid = [[' '] * dims[0] for i in range(dims[1])]
        if a == '':
            i += 1
        else:
            i -= 1
        for robot in robots:
            p, v = robot
            if a == '':
                new_p = p + v
            else:
                new_p = p - v
            new_x = int(new_p.real) % dims[0]
            new_y = int(new_p.imag) % dims[1]
            grid[new_y][new_x] = '.'
            robot[0] = complex(new_x, new_y)

        x_mid = dims[0] // 4
        y_mid = dims[1] // 4
        qs = [0]*4
        for p, _ in robots:
            x = int(p.real)
            y = int(p.imag)
            if x_mid <= x <= dims[0]-x_mid or y_mid <= y <= dims[1]-y_mid:
                continue

            q_idx = 0
            if x > x_mid:
                q_idx += 1
            if y > y_mid:
                q_idx += 2
            qs[q_idx] += 1

        res = 1
        for q in qs:
            res *= q
        reses.append(math.log(res))
        if res < 1100:
            print(i, res)
            for row in grid:
                print(' '.join(row))
            a = input()
    #plt.axvline(6398, color='red', linestyle='-')
    #plt.plot(reses)
    #plt.show()
    for row in grid:
        print(' '.join(row))

    print(res)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

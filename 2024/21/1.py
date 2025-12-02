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

'''
789
456
123
 0A

 ^A
<v>
'''

KEYPAD = {
    '0': 3+1j,
    'A': 3+2j,
    '1': 2+0j,
    '2': 2+1j,
    '3': 2+2j,
    '4': 1+0j,
    '5': 1+1j,
    '6': 1+2j,
    '7': 0+0j,
    '8': 0+1j,
    '9': 0+2j,
}

ARROW = {
    '^': 0+1j,
    'A': 0+2j,
    '<': 1+0j,
    'v': 1+1j,
    '>': 1+2j,
}

DIRS = {
    '^': -1,
    '>': 1j,
    'v': 1,
    '<': -1j,
}

LEFT = '<'
UP = '^'
RIGHT = '>'
DOWN = 'v'
PRESS = 'A'


def main(test=False):
    codes = []
    with open("test.txt" if test else "input.txt") as f:
        for line in f:
            codes.append(line.strip())

    def get_dirs(coords):
        y = int(coords.real)
        x = int(coords.imag)
        dirs = defaultdict(int)
        if y < 0:
            dirs[UP] = abs(y)
        if y > 0:
            dirs[DOWN] = abs(y)
        if x < 0:
            dirs[LEFT] = abs(x)
        if x > 0:
            dirs[RIGHT] = abs(x)
        return dirs

    def dist_keypad(dir, coord2):
        if dir == LEFT:
            return 1
        if dir == DOWN:
            return 2
        return 3

    def dist_arrow(dir, coord2):
        if dir == LEFT:
            return 1
        if dir == DOWN:
            return 2
        return 3

    def press_keypad(code):
        start = KEYPAD['A']
        moves = []
        last = start
        for dig in code:
            move = KEYPAD[dig] - last
            dirs = get_dirs(move)
            std = list(sorted(dirs.keys(), key=lambda x: dist_keypad(x, last)))
            if len(std) > 0 and last + DIRS[std[0]] * dirs[std[0]] == 3:
                std = reversed(std)
            for dir in std:
                for i in range(dirs[dir]):
                    moves.append(dir)
            moves.append(PRESS)
            last = KEYPAD[dig]

        score = defaultdict(int)
        for transition in zip(['A'] + moves[:-1], moves):
            score[transition] += 1
        return score

    cache = {}
    def press_arrow(in_moves):
        start = ARROW['A']
        moves = []
        last = start
        #print(in_moves)
        for dig in in_moves:
            move = ARROW[dig] - last
            if (ARROW[dig], last) in cache:
                moves += cache[(ARROW[dig], last)]
                last = ARROW[dig]
            dirs = get_dirs(move)
            std = list(sorted(dirs.keys(), key=lambda x: dist_arrow(x, last)))
            if len(std) > 0 and last + DIRS[std[0]] * dirs[std[0]] == 0:
                std = reversed(std)
            this_moves = []
            for dir in std:
                for i in range(dirs[dir]):
                    this_moves.append(dir)
            this_moves.append(PRESS)
            #print(' ', this_moves)
            cache[(ARROW[dig], last)] = this_moves
            moves += this_moves
            last = ARROW[dig]
        return moves

    trans_cache = {}
    res = 0
    for code in codes:
        print(code)
        score = press_keypad(code)
        print(' ', dict(score))
        for i in range(25):
            new_score = defaultdict(int)
            for transition, t_count in score.items():
                if transition in trans_cache:
                    counter = trans_cache[transition]
                    for t, c in counter.items():
                        new_score[t] += c * t_count
                    continue

                f, t = transition
                move = ARROW[t] - ARROW[f]
                dirs = get_dirs(move)
                std = list(sorted(dirs.keys(), key=lambda x: dist_arrow(x, f)))
                if len(std) > 0 and ARROW[f] + DIRS[std[0]] * dirs[std[0]] == 0:
                    std = reversed(std)
                this_moves = []
                for dir in std:
                    for i in range(dirs[dir]):
                        this_moves.append(dir)
                this_moves.append(PRESS)
                this_counter = defaultdict(int)
                for inner in zip(['A'] + this_moves[:-1], this_moves):
                    new_score[inner] += t_count
                    this_counter[inner] += 1
                trans_cache[transition] = this_counter
            score = new_score
            print(' ', dict(score))
        print('   ', dict(trans_cache[('^', '>')]))

        res2 = 0
        for v in score.values():
            res2 += v
        print(code, res)
        res += int(code[:-1]) * res2
    print(res)
    #print(codes[4])
    #print('A '.join((''.join(press_keypad(codes[4]))).split('A')))
    #print('A '.join((''.join(press_arrow(press_keypad(codes[4])))).split('A')))
    #print('A '.join((''.join(press_arrow(press_arrow(press_keypad(codes[4]))))).split('A')))
    #print(len(press_arrow(press_arrow(press_keypad(codes[4])))))

    # 186046 too high


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

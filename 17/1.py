#!/usr/bin/env python3
import json
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


class Machine:
    def __init__(self, reg_a, reg_b, reg_c, program):
        self.reg_a = reg_a
        self.reg_b = reg_b
        self.reg_c = reg_c
        self.program = program
        self.output = []
        self.did_jump = False
        self.ip = 0

    def combo(self, x):
        match x:
            case 0:
                return 0
            case 1:
                return 1
            case 2:
                return 2
            case 3:
                return 3
            case 4:
                return self.reg_a
            case 5:
                return self.reg_b
            case 6:
                return self.reg_c
        return None

    def op0(self, x):
        self.reg_a = (self.reg_a >> self.combo(x))

    def op1(self, x):
        self.reg_b = (self.reg_b ^ x)

    def op2(self, x):
        self.reg_b = self.combo(x) % 8

    def op3(self, x):
        self.ip = x if self.reg_a != 0 else self.ip
        if self.reg_a != 0:
            self.did_jump = True

    def op4(self, x):
        self.reg_b = self.reg_b ^ self.reg_c

    def op5(self, x):
        return self.combo(x) % 8

    def op6(self, x):
        self.reg_b = (self.reg_a >> self.combo(x))

    def op7(self, x):
        self.reg_c = (self.reg_a >> self.combo(x))

    def run(self):
        while self.ip < len(self.program)-1:
            op_id = self.program[self.ip]
            arg = self.program[self.ip+1]
            match op_id:
                case 0:
                    self.op0(arg)
                case 1:
                    self.op1(arg)
                case 2:
                    self.op2(arg)
                case 3:
                    self.op3(arg)
                case 4:
                    self.op4(arg)
                case 5:
                    yield self.op5(arg)
                case 6:
                    self.op6(arg)
                case 7:
                    self.op7(arg)
            if not self.did_jump:
                self.ip += 2
            self.did_jump = False
        return self.output


def main(test=False):
    reg_a = None
    reg_b = None
    reg_c = None
    program = None
    with open("test.txt" if test else "input.txt") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            label, value = line.strip().split(':')
            match label:
                case 'Register A':
                    reg_a = int(value.strip())
                case 'Register B':
                    reg_b = int(value.strip())
                case 'Register C':
                    reg_c = int(value.strip())
                case 'Program':
                    program = [int(v) for v in value.strip().split(',')]

    cache = {}
    init_val = 105981155568026
    while True:
        #if ((init_val & 7) ^ 1) != init_val >> ((init_val & 7) ^ 5):
        #    init_val += 1
        #    continue
        print(init_val, len(cache))
        shift = 0
        found = True
        cache_miss = False
        for dig in program:
            last_10 = f"{init_val >> shift:#012b}"[-10:]
            if last_10 not in cache:
                cache_miss = True
                found = False
                break
            if cache[last_10] != dig:
                found = False
                break
            shift += 3
        if found:
            print("FOUND")
            break
        
        if cache_miss:
            print("CACHE MISS")
            m = Machine(init_val, 0, 0, program)
            p_idx = 0
            shift = 0
            is_good = True
            for dig in m.run():
                last_10 = f"{init_val >> shift:#012b}"[-10:]
                if last_10 in cache:
                    print('hit', init_val, len(cache))
                    assert dig == cache[last_10]
                else:
                    cache[last_10] = dig
                shift += 3
                if p_idx >= len(program) or dig != program[p_idx]:
                    is_good = False
                    break
                p_idx += 1
            if is_good and p_idx == len(program):
                print('good', init_val)
                break
        init_val += 1



if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

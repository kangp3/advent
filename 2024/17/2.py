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


def main(test=False):
    # Load precomputed cache (binary 10-digit numbers -> 3-bit digit produced)
    with open('cache.json') as cache_f:
        cache = json.load(cache_f)

    # Reverse the program and work from the end
    program = # REDACTED??
    rev_prog = list(reversed(program))

    # Create two lookups
    # This one maps from a 7-digit prefixes to all keys that start with that prefix
    begs7 = defaultdict(set)
    # This one maps from 3-bit digits to all keys that produce that digit
    reved = defaultdict(set)
    for k, v in cache.items():
        reved[v].add(k)
        begs7[k[:-3]].add(k)

    # Recurse (Center (?))
    #   - program is the program thus far
    #   - prev is the digits so far
    def recurse_maybe(program, prev=None):
        # The current op is the first thing in the (reversed) program
        op = program[0]
        if len(program) == 1:
            # If we're on the last (first?) op then grab the smallest value that
            #  smallest value that matches the op and starts with the last 7 digits
            #  of what we have so far
            for k in sorted(begs7[prev[-7:]]):
                if cache[k] == op:
                    return k
            return None

        # If we haven't built up any digits yet then just try every 10-digit number
        #  that maps to the first digit in ascending order
        if prev is None:
            for i in sorted(reved[op]):
                soln = recurse_maybe(program[1:], prev=i)
                if soln is not None:
                    return i[:3] + soln
            return None

        # If we have built up digits then try every 10-digit number that starts
        #  with the last 7-digits of the digits we have so far and matches our op
        for k in sorted(begs7[prev[-7:]]):
            if cache[k] == op:
                soln = recurse_maybe(program[1:], prev=k)
                if soln is not None:
                    return k[:3] + soln
        return None

    print(recurse_maybe(rev_prog))

    return
    digs = ''
    found = False
    for i in sorted(reved[0]):
        for k in sorted(begs7[i[3:]]):
            if cache[k] == 3:
                print(0, 3, i, k)
                found = True
                digs += i
                break
        if found:
            break
    for op, nop in zip(rev_prog[1:-1], rev_prog[2:]):
        for k in sorted(begs7[digs[-7:]]):
            print(op, nop, k, cache[k])
            if cache[k] == nop:
                print(op, nop, digs, k)
                found = True
                digs += i[-3:]
                break
        if found:
            break
    for k in sorted(begs7[digs[-7:]]):
        if cache[k] == 2:
            print(2, None, digs, k)
            digs += k[-3:]
            break
    print(digs)

    print(digs)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

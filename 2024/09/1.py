#!/usr/bin/env python3
import argparse
from collections import *
import re


def main(test=False):
    digs = []
    with open("test.txt" if test else "input.txt") as f:
        for line in f:
            digs = [int(c) for c in line.strip()]

    memory = []
    is_file = True
    file_idx = 0
    for v in digs:
        for i in range(v):
            if is_file:
                memory.append(file_idx)
            else:
                memory.append('.')
        if is_file:
            file_idx += 1
        is_file = not is_file

    new_len = len(memory)
    end_idx = len(memory)-1
    start_idx = 0
    while start_idx < len(memory):
        while start_idx < len(memory) and memory[start_idx] != '.':
            start_idx += 1
        while start_idx < len(memory) and memory[start_idx] == '.':
            if memory[end_idx] != '.':
                memory[start_idx] = memory[end_idx]
                new_len -= 1
                start_idx += 1
            end_idx -= 1

    res = 0
    for idx, fid in enumerate(memory[:new_len]):
        res += idx * fid
    print(res)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

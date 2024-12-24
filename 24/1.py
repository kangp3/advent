#!/usr/bin/env python3
from random import randrange
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


class Node:
    def __init__(self, name):
        self.name = name
        self.op = None
        self.l = None
        self.r = None
        self.val = None
        self.parents = set()

    def __eq__(self, o):
        return self.name == o.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        l = self.l.name if self.l else ' '
        r = self.r.name if self.r else ' '
        op = 'None'
        match self.op:
            case 'AND':
                op = '&'
            case 'OR':
                op = '|'
            case 'XOR':
                op = '^'
        return f'({self.name}: {self.val} ({l} {op} {r}))'


def main(test=False):
    inputs = {}
    nodes = dict()
    xs = []
    ys = []
    max_z = 0

    is_inputs = True
    is_x_input = True
    with open("test.txt" if test else "input.txt") as f:
        for line in f:
            line = line.strip()
            if not line:
                is_inputs = False
                continue
            if is_inputs:
                k, v = line.split(': ')
                inputs[k] = int(v)
                nodes[k] = Node(k)
                nodes[k].val = int(v)
                if k[0] == 'y':
                    is_x_input = False
                if is_x_input:
                    xs.append(int(v))
                else:
                    ys.append(int(v))
            else:
                ops, res = line.split(' -> ')
                l, op, r = ops.split(' ')
                # These prints let me | pbcopy into the GraphViz tool: https://dreampuf.github.io/GraphvizOnline
                print(f'{res} -> {l};')
                print(f'{res} -> {r};')
                if l not in nodes:
                    nodes[l] = Node(l)
                if r not in nodes:
                    nodes[r] = Node(r)
                if res not in nodes:
                    nodes[res] = Node(res)
                nodes[res].op = op
                # Ditto, GraphViz prints
                match op:
                    case 'AND':
                        print(f'{res} [shape="rectangle"];')
                    case 'OR':
                        print(f'{res} [shape="pentagon"];')
                    case 'XOR':
                        print(f'{res} [shape="hexagon"];')
                nodes[res].l = nodes[l]
                nodes[res].r = nodes[r]
                nodes[l].parents.add(res)
                nodes[r].parents.add(res)
                if res[0] == 'z':
                    z_val = int(res[1:])
                    if z_val > max_z:
                        max_z = z_val

    def calc(n):
        if n.val:
            return
        if n.l and n.l.val is None:
            calc(n.l)
        if n.r and n.r.val is None:
            calc(n.r)
        #print(n)
        match n.op:
            case 'OR':
                n.val = n.l.val | n.r.val
            case 'AND':
                n.val = n.l.val & n.r.val
            case 'XOR':
                n.val = n.l.val ^ n.r.val

    def calc_res(nodes):
        roots = set()
        for i in nodes.values():
            if not i.parents:
                roots.add(i)

        for root in roots:
            #print('r', root)
            calc(root)

        zs = [None] * (max_z+1)
        for name, node in nodes.items():
            if name[0] == 'z':
                z_val = int(name[1:])
                zs[z_val] = node.val

        #print(list(zs))
        res = 0
        for z in reversed(zs):
            res = (res << 1) + z
        return res

    def test_z(node, nodes):
        num = int(node.name[1:])

        or_node = None
        xor_node = None
        if node.l.op == 'OR':
            or_node = node.l
            xor_node = node.r
        if node.r.op == 'OR':
            or_node = node.r
            xor_node = node.l
        if or_node is None:
            return "MISSING OR"
        if xor_node is None:
            return "MISSING XOR"
        if or_node.op != 'OR':
            return f"OR NODE OP WRONG: {or_node.op}"
        if xor_node.op != 'XOR':
            return f"XOR NODE OP WRONG: {xor_node.op}"

        xor_x_node = None
        xor_y_node = None
        if xor_node.l.name.startswith('x'):
            xor_x_node = xor_node.l
            xor_y_node = xor_node.r
        if xor_node.r.name.startswith('x'):
            xor_x_node = xor_node.r
            xor_y_node = xor_node.l
        if xor_x_node is None:
            return "MISSING XOR X"
        if xor_y_node is None:
            return "MISSING XOR Y"
        if xor_x_node.name != f'x{num:02}':
            return f"BAD XOR X: {xor_x_node.name}"
        if xor_y_node.name != f'y{num:02}':
            return f"BAD XOR Y: {xor_x_node.name}"

        if or_node.l.op != 'AND':
            return f"BAD OR L OP: {or_node.l.op}"
        if or_node.r.op != 'AND':
            return f"BAD OR R OP: {or_node.l.op}"

        or_and_in = None
        or_and_recursive = None
        if or_node.l.l.name in (f'x{num-1:02}', f'y{num-1:02}'):
            or_and_in = or_node.l
            or_and_recursive = or_node.r
        if or_node.r.l.name in (f'x{num-1:02}', f'y{num-1:02}'):
            or_and_in = or_node.r
            or_and_recursive = or_node.l
        if or_and_in is None:
            return "MISSING OR AND IN SIDE"
        if or_and_recursive is None:
            return "MISSING OR AND RECURSIVE SIDE"

        x0_in = None
        y0_in = None
        if or_and_in.l.name == f'x{num-1:02}':
            x0_in = or_and_in.l
            y0_in = or_and_in.r
        if or_and_in.r.name == f'x{num-1:02}':
            x0_in = or_and_in.r
            y0_in = or_and_in.l
        if x0_in is None:
            return "MISSING OR AND IN X"
        if y0_in is None:
            return "MISSING OR AND IN Y"
        if x0_in.name != f'x{num-1:02}':
            return f"BAD OR AND IN X: {x0_in.name}"
        if y0_in.name != f'y{num-1:02}':
            return f"BAD OR AND IN Y: {y0_in.name}"

        or_and_xor = None
        or_and_or = None
        if or_and_recursive.l.op == 'XOR':
            or_and_xor = or_and_recursive.l
            or_and_or = or_and_recursive.r
        if or_and_recursive.r.op == 'XOR':
            or_and_xor = or_and_recursive.r
            or_and_or = or_and_recursive.l
        if or_and_xor is None:
            return "MISSING OR AND XOR:"
        if or_and_or is None:
            return "MISSING OR AND OR:"
        if or_and_xor.op != 'XOR':
            return f"BAD OR AND XOR OP: {or_and_xor.op}"
        if or_and_or.op != 'OR':
            return f"BAD OR AND OR OP: {or_and_or.op}"

        or_and_xor_x = None
        or_and_xor_y = None
        if or_and_xor.l.name == x0_in.name:
            or_and_xor_x = or_and_xor.l
            or_and_xor_y = or_and_xor.r
        if or_and_xor.r.name == x0_in.name:
            or_and_xor_x = or_and_xor.r
            or_and_xor_y = or_and_xor.l
        if or_and_xor_x.name != x0_in.name:
            return f"BAD OR AND XOR X: {or_and_xor_x.name} {x0_in.name}"
        if or_and_xor_y.name != y0_in.name:
            return f"BAD OR AND XOR Y: {or_and_xor_y.name} {y0_in.name}"

        z0 = nodes[f'z{num-1:02}']
        z0_xor = None
        z0_or = None
        if z0.l.op == 'XOR':
            z0_xor = z0.l
            z0_or = z0.r
        if z0.r.op == 'XOR':
            z0_xor = z0.r
            z0_or = z0.l
        if z0_xor.name != or_and_xor.name:
            return f"BAD z0 XOR: {z0_xor.name} {or_and_xor.name}"
        if z0_or.name != or_and_or.name:
            return f"BAD z0 OR: {z0_or.name} {or_and_or.name}"

        return None

    # Test all the z-nodes' structures
    for name, node in sorted(nodes.items()):
        if name[0] == 'z' and int(name[1:]) > 2:
            check = test_z(node, nodes)
            if check is not None:
                print(name, check)


    #x = 0
    #for x_dig in reversed(xs):
    #    x = (x << 1) + x_dig

    #y = 0
    #for y_dig in reversed(ys):
    #    y = (y << 1) + y_dig


    # Fuzz the graph to find bad digits
    #bad_bits = set()
    #for i in range(500):
    #    new_nodes = deepcopy(nodes)
    #    x = randrange(2 ** len(xs))
    #    y = randrange(2 ** len(ys))
    #    expected = x + y
    #    for idx, dig in enumerate(reversed(f"{x:0{len(xs)}b}")):
    #        new_nodes[f'x{idx:02}'].val = int(dig)
    #    for idx, dig in enumerate(reversed(f"{y:0{len(ys)}b}")):
    #        new_nodes[f'y{idx:02}'].val = int(dig)
    #    res = calc_res(new_nodes)

    #    diff = expected ^ res
    #    for idx, dig in enumerate(reversed(bin(diff)[2:])):
    #        if dig == '1':
    #            bad_bits.add(idx)

    #print(len(bad_bits), sorted(bad_bits))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

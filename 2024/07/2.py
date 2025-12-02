#!/usr/bin/env python3
import argparse
from collections import *
import re


def main(test=False):
    with open("test.txt" if test else "input.txt") as f:
        for line in f:
            pass


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--test", action=argparse.BooleanOptionalAction)
    args = ap.parse_args()

    main(test=args.test)

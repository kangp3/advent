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
    files = set()
    is_file = True
    file_idx = 0
    for v in digs:
        if is_file:
            files.add((file_idx, v))
            memory.append((file_idx, v))
        else:
            memory.append((None, v))
        if is_file:
            file_idx += 1
        is_file = not is_file

    sorted_fs = sorted(files, reverse=True)
    moved_fids = set()
    while True:
        #print(memory)
        reached_end = True
        for f_idx, info in list(enumerate(memory))[::-1]:
            fid, req_mem = info
            if fid is None or fid in moved_fids:
                continue
            reached_end = False
            break
        #print(f"{fid=}, {req_mem=}")
        if reached_end:
            break
        for m_idx, info in enumerate(memory[:f_idx]):
            none_fid, ava_mem = info
            #print(f"{m_idx=}, {none_fid=}, {ava_mem=}")
            if none_fid is not None:
                continue
            if ava_mem < req_mem:
                continue
            #print("BEFORE", memory, m_idx, ava_mem, f_idx, fid, req_mem)
            memory[f_idx] = (None, req_mem)
            memory[m_idx] = (fid, req_mem)
            memory.insert(m_idx+1, (None, ava_mem - req_mem))
            #print("AFTER", memory, m_idx, ava_mem, f_idx, fid, req_mem)
            break
        moved_fids.add(fid)
    print(memory)

    res = 0
    m_idx = 0
    for f_idx, v in memory:
        for i in range(v):
            f_idx = 0 if f_idx is None else f_idx
            res += f_idx * m_idx
            m_idx += 1
    print(res)
    return
        
    old_idx = len(memory)-1
    for fid, v in memory[::-1]:
        #print((fid, v, old_idx))
        if fid is None:
            old_idx -= 1
            continue
        if fid in moved_fids:
            old_idx -= 1
            continue
        for idx, info in enumerate(memory):
            none_fid, free_mem = info
            if none_fid is not None:
                continue
            if free_mem >= v:
                memory[idx] = (fid, v)
                memory[old_idx] = (None, v)
                memory.insert(idx, (None, free_mem-v))
                old_idx += 1
                break
        old_idx -= 1
    print(memory)
    return

    new_mem = []
    m_idx = 0
    while m_idx < len(memory):
        if memory[m_idx][0] is None:
            fs = sorted(files, reverse=True)
            for fid, v in fs:
                if v <= memory[m_idx][1]:
                    print(f"{fid=} {v=} {memory[m_idx][1]=}")
                    new_mem.append((fid, v))
                    new_mem.append((None, memory[m_idx][1] - v))
                    files.remove((fid, v))
                    break
        else:
            print(f"{memory[m_idx]=}")
            new_mem.append(memory[m_idx])
        m_idx += 1
    print(new_mem)
    return

    

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

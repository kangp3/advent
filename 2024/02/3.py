#!/usr/bin/env python

with open('3.txt') as f:
    safe = 0
    for row in f:
        orig_elts = [int(elt) for elt in row.split()]
        candidates = [orig_elts]
        for skip_idx in range(len(orig_elts)):
            candidates.append(orig_elts[:skip_idx] + orig_elts[skip_idx+1:])
        
        is_safe = False
        for elts in candidates:
            inc = None
            last = None
            is_safe = True
            for curr in elts:
                if last is None:
                    last = curr
                    continue
        
                is_first = False
                if inc is None:
                    is_first = True
                    inc = last < curr
                if inc:
                    diff = curr - last
                else:
                    diff = last - curr
                if diff < 1 or diff > 3:
                    is_safe = False
                    break
                last = curr
        
            if is_safe:
                safe += 1
                break
        #print(elts, is_safe, inc)

        elts = orig_elts
        bad_safe = 0
        inc = int(elts[0]) < int(elts[1])
        last = int(elts[0])
        did_skip = False
        is_bad_safe = True
        for elt in elts[1:]:
            curr = int(elt)
            if inc:
                diff = curr - last
            else:
                diff = last - curr
            if diff < 1 or diff > 3:
                if not did_skip:
                    did_skip = True
                    continue
                is_bad_safe = False
                break
            last = curr
        
        if not is_bad_safe:
            elts = elts[1:]
            inc = int(elts[0]) < int(elts[1])
            last = int(elts[0])
            is_bad_safe = True
            for elt in elts[1:]:
                curr = int(elt)
                if inc:
                    diff = curr - last
                else:
                    diff = last - curr
                if diff < 1 or diff > 3:
                    is_bad_safe = False
                    break
                last = curr
        if is_bad_safe:
            bad_safe += 1
        if is_safe != is_bad_safe:
            print("DISAGREE", orig_elts)
    print(safe)
    print(bad_safe)

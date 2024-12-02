#!/usr/bin/env python
import re
import sys
import timeit
from collections import Counter


def parse(L: list[str]) -> tuple[Counter[int], Counter[int]]:
    left = []
    right = []
    for s in L:
        (a, b) = re.findall(r"\d+", s)
        left.append(int(a))
        right.append(int(b))
    return Counter(left), Counter(right)


def solve(left: Counter[int], right: Counter[int]) -> int:
    return sum(k * left[k] * right[k] for k in left)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    if argv[0] == "python":
        argv = argv[1:]
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    L_left, L_right = parse(L)
    start = timeit.default_timer()
    print(solve(L_left, L_right))
    stop = timeit.default_timer()
    print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

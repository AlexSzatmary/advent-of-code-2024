#!/usr/bin/env python
import re
import sys
import timeit


def parse(L: list[str]) -> tuple[list[int], list[int]]:
    L_left = []
    L_right = []
    for s in L:
        (a, b) = re.findall(r"\d+", s)
        L_left.append(int(a))
        L_right.append(int(b))
    return sorted(L_left), sorted(L_right)


def solve(L_left, L_right):
    return sum(abs(a - b) for (a, b) in zip(L_left, L_right))


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

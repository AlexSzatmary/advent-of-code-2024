#!/usr/bin/env python
import sys
import timeit
from itertools import pairwise


def parse(L: list[str]) -> list[list[int]]:
    return [list(map(int, line.split())) for line in L]


def is_safe(report: list[int]) -> bool:
    if report[0] < report[1]:
        return all(1 <= b - a <= 3 for (a, b) in pairwise(report))
    else:
        return all(1 <= a - b <= 3 for (a, b) in pairwise(report))


def solve(reports: list[list[int]]) -> int:
    return sum(map(is_safe, reports))


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv
    if argv[0] == "python":
        argv = argv[1:]
    with open(argv[1]) as hin:
        L = hin.readlines()
    reports = parse(L)
    start = timeit.default_timer()
    print(solve(reports))
    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

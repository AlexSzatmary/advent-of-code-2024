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


def is_safe_with_dampener(report: list[int]) -> bool:
    def is_ascending(report: list[int], i: int) -> bool:
        return 1 <= report[i + 1] - report[i] <= 3

    def is_descending(report: list[int], i: int) -> bool:
        return 1 <= report[i] - report[i + 1] <= 3

    for condition in [is_ascending, is_descending]:
        first_bad_level_index = -1
        for i in range(len(report) - 1):
            if not condition(report, i):
                first_bad_level_index = i
        if first_bad_level_index == -1:
            return True
        if is_safe(
            report[:first_bad_level_index] + report[first_bad_level_index + 1 :]
        ):
            return True
        if is_safe(
            report[: first_bad_level_index + 1] + report[first_bad_level_index + 2 :]
        ):
            return True
    return False


def solve(reports: list[list[int]]) -> int:
    return sum(map(is_safe_with_dampener, reports))


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

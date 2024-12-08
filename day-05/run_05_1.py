#!/usr/bin/env python
import sys
import timeit


def parse(L: list[str]) -> tuple[list[tuple[int, int]], list[list[int]]]:
    rules = []
    updates = []
    for s in L:
        if "|" in s:
            rules.append(tuple(map(int, s.split("|"))))
        elif "," in s:
            updates.append(list(map(int, s.split(","))))
    return rules, updates


def check_update(rules: list[tuple[int, int]], update: list[int]) -> bool:
    for before, after in rules:
        if before in update and after in update:
            if update.index(before) > update.index(after):
                return False
    return True


def solve(rules: list[tuple[int, int]], updates: list[list[int]]) -> int:
    return sum(
        update[(len(update) - 1) // 2]
        for update in updates
        if check_update(rules, update)
    )


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv
    if argv[0] == "python":
        argv = argv[1:]
    with open(argv[1]) as hin:
        L = hin.readlines()
    rules, updates = parse(L)
    start = timeit.default_timer()
    print(solve(rules, updates))
    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

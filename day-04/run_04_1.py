#!/usr/bin/env python
import numpy as np
import sys
import timeit


def parse(L: list[str]) -> np.ndarray:
    return np.array([[ord(c) for c in s[:-1]] for s in L])


def pprint_crossword(crossword: np.ndarray) -> None:
    print("\n".join("".join([chr(c) for c in row]) for row in crossword))


def solve(crossword: np.ndarray) -> int:
    XMAS = np.array([ord(c) for c in "XMAS"])
    SMAX = XMAS[::-1]
    count = 0
    for i in range(0, crossword.shape[0]):
        for j in range(0, crossword.shape[1] - 3):
            count += np.all(crossword[i, j : j + 4] == XMAS)
            count += np.all(crossword[i, j : j + 4] == SMAX)
    for i in range(-(crossword.shape[0] - 4), crossword.shape[1] - 3):
        diag = np.diagonal(crossword, i)
        for j in range(0, diag.size - 3):
            count += np.all(diag[j : j + 4] == XMAS)
            count += np.all(diag[j : j + 4] == SMAX)
    crossword = np.rot90(crossword)
    for i in range(0, crossword.shape[0]):
        for j in range(0, crossword.shape[1] - 3):
            count += np.all(crossword[i, j : j + 4] == XMAS)
            count += np.all(crossword[i, j : j + 4] == SMAX)
    for i in range(-(crossword.shape[0] - 4), crossword.shape[1] - 3):
        diag = np.diagonal(crossword, i)
        for j in range(0, diag.size - 3):
            count += np.all(diag[j : j + 4] == XMAS)
            count += np.all(diag[j : j + 4] == SMAX)
    return count


def main(argv=None):
    if argv is None:
        argv = sys.argv
    if argv[0] == "python":
        argv = argv[1:]
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    crossword = parse(L)
    start = timeit.default_timer()
    print(solve(crossword))
    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

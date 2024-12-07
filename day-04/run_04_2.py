#!/usr/bin/env python
import numpy as np
import sys
import timeit


def parse(L: list[str]) -> np.ndarray:
    return np.array([[ord(c) for c in s[:-1]] for s in L])


def pprint_crossword(crossword: np.ndarray) -> None:
    print("\n".join("".join([chr(c) for c in row]) for row in crossword))


def solve(crossword: np.ndarray) -> int:
    A = ord("A")
    M = ord("M")
    S = ord("S")
    MMSS = np.array([[M, M], [S, S]])
    MSMS = np.rot90(MMSS)
    SSMM = np.rot90(MSMS)
    SMSM = np.rot90(SSMM)
    count = 0
    for i in range(1, crossword.shape[0] - 1):
        for j in range(1, crossword.shape[1] - 1):
            if crossword[i, j] == A:
                square = crossword[i - 1 : i + 2 : 2, j - 1 : j + 2 : 2]
                count += np.all(square == MMSS)
                count += np.all(square == MSMS)
                count += np.all(square == SSMM)
                count += np.all(square == SMSM)
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

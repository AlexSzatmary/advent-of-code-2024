import numpy as np
import sys
import timeit


def parse(lines: list[str]) -> tuple[np.ndarray, np.ndarray]:
    """
    Given input, creates network

    Parameters
    ----------
    lines : text of input file as list of strings

    Returns
    -------
    locks : 2D np array, num_locks x 5, heights of lock columns
    keys : 2D np array, num_keys x 5, heights of key columns
    """
    locks = []  # build the arrays using list.append and then convert to arrays
    keys = []
    rows_per_item = 8  # include newline
    for i in range((len(lines) + 1) // rows_per_item):
        start_row = i * rows_per_item
        if lines[start_row][0] == "#":  # lock
            heights = np.zeros(5, dtype=int)
            for j in range(1, rows_per_item - 2):  # ignore irrelevant lines
                row = lines[start_row + j]
                for k in range(5):
                    if row[k] == "#":
                        heights[k] = j
            locks.append(heights)
        else:  # key
            heights = np.zeros(5, dtype=int)
            for j in range(1, rows_per_item - 2):  # ignore irrelevant lines
                row = lines[start_row + rows_per_item - j - 2]
                for k in range(5):
                    if row[k] == "#":
                        heights[k] = j
            keys.append(heights)
    return np.array(locks), np.array(keys)


def count_fits(locks: np.ndarray, keys: np.ndarray) -> list[tuple[int, int]]:
    fits = []
    for i, lock in enumerate(locks):
        for j, key in enumerate(keys):
            if np.all(lock + key <= 5):
                fits.append((i, j))
    return fits


def solve_1(locks: np.ndarray, keys: np.ndarray) -> int:
    return len(count_fits(locks, keys))


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv
    if argv[0] == "python":
        argv = argv[1:]
    with open(argv[-1]) as hin:
        input_lines = hin.readlines()
    locks, keys = parse(input_lines)
    start = timeit.default_timer()
    if "1" in argv:
        print(solve_1(locks, keys))

    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

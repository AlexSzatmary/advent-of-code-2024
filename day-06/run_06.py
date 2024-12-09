from typing import assert_never
import numpy as np
import re
import sys
import timeit


def parse(input_lines: list[str]) -> np.ndarray:
    obstacles = np.zeros((len(input_lines), len(input_lines[0]) - 1), dtype=np.bool_)
    for i, line in enumerate(input_lines):
        obstacles[i, [m.start() for m in re.finditer(r"#", line)]] = True
        if (j := line.find("^")) != -1:
            start_i = i
            start_j = j
    return obstacles, (start_i, start_j)


def solve_1(obstacles: np.ndarray, start_ij: tuple[int, int]) -> int:
    i, j = start_ij
    visited = np.zeros(obstacles.shape, dtype=np.bool_)
    # visited[i, j] = True
    direction = 1  # north; directions are 0 east, 1 north, 2 west, 3 south
    di = -1
    dj = 0
    while True:
        visited[i, j] = True
        next_i = i + di
        next_j = j + dj
        if (
            next_i < 0
            or next_j < 0
            or next_i >= obstacles.shape[0]
            or next_j >= obstacles.shape[1]
        ):
            break
        if obstacles[next_i, next_j]:
            direction = (direction - 1) % 4
            match direction:
                case 0:
                    di, dj = 0, 1
                case 1:
                    di, dj = -1, 0
                case 2:
                    di, dj = 0, -1
                case 3:
                    di, dj = 1, 0
                case _:  # pragma: no cover. Unreachable.
                    assert_never(direction)
        else:
            i, j = next_i, next_j
    return np.sum(visited)


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv
    if argv[0] == "python":
        argv = argv[1:]
    with open(argv[-1]) as hin:
        input_lines = hin.readlines()
    rules, updates = parse(input_lines)
    start = timeit.default_timer()
    if "1" in argv:
        print(solve_1(rules, updates))
    elif "2" in argv:
        pass
    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

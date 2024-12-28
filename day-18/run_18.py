from heapq import heappush, heappop
import numpy as np
import sys
import timeit


def parse_1(lines: list[str]) -> np.ndarray:
    if len(lines) > 1024:
        size = 73
        fallen_bytes = 1024
    else:
        size = 9
        fallen_bytes = 12
    walls = np.ones((size, size), dtype=bool)
    walls[1:-1, 1:-1] = False
    for line in lines[:fallen_bytes]:
        j, i = line[:-1].split(",")
        walls[int(i) + 1, int(j) + 1] = True
    return walls


def walk(walls: np.ndarray) -> np.ndarray:
    path = walls.size * np.ones_like(walls, dtype=int)
    path[1, 1] = 0
    min_step = walls.size
    edges = [(0, 1, 1)]
    while edges:
        step, i, j = heappop(edges)
        if step >= min_step:
            break
        if (i, j) == (walls.shape[0] - 2, walls.shape[1] - 2):
            min_step = min(min_step, step)
        for di, dj in [(0, 1), (-1, 0), (0, -1), (1, 0)]:
            if not walls[i + di, j + dj] and step + 1 < path[i + di, j + dj]:
                path[i + di, j + dj] = step + 1
                heappush(edges, (step + 1, i + di, j + dj))
    return path


def solve_1(walls: np.ndarray) -> int:
    return walk(walls)[-2, -2]


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv
    if argv[0] == "python":
        argv = argv[1:]
    with open(argv[-1]) as hin:
        input_lines = hin.readlines()
    walls = parse_1(input_lines)
    start = timeit.default_timer()
    if "1" in argv:
        print(solve_1(walls))

    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

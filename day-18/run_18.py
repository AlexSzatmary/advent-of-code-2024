from heapq import heappush, heappop
import numpy as np
import sys
import timeit


def parse(lines: list[str]) -> np.ndarray:
    return np.array([list(map(int, line[:-1].split(","))) for line in lines], dtype=int)


def drop_n_bytes(wall_ij: np.ndarray, size: int, n_bytes: int) -> np.ndarray:
    walls = np.ones((size, size), dtype=bool)
    walls[1:-1, 1:-1] = False
    for wall in wall_ij[:n_bytes]:
        walls[wall[1] + 1, wall[0] + 1] = True
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


def size_n_bytes(wall_ij: np.ndarray) -> tuple[int, int]:
    if len(wall_ij) > 1024:
        size = 73
        fallen_bytes = 1024
    else:
        size = 9
        fallen_bytes = 12
    return size, fallen_bytes


def solve_1(wall_ij: np.ndarray) -> int:
    size, fallen_bytes = size_n_bytes(wall_ij)
    walls = drop_n_bytes(wall_ij, size, fallen_bytes)
    return walk(walls)[-2, -2]


def render_walls_path(walls: np.ndarray, path: np.ndarray) -> str:
    big_num = walls.size
    rows = []
    for i in range(walls.shape[0]):
        rows.append(
            "".join(
                "#"
                if walls[i, j]
                else str(path[i, j] % 10)
                if path[i, j] < big_num
                else "."
                for j in range(walls.shape[1])
            )
        )
    return "\n".join(rows)


def solve_2(wall_ij: np.ndarray) -> str:
    """
    Solves using the bisection algorithm
    """
    size, _fallen_bytes = size_n_bytes(wall_ij)
    a = 0
    c = len(wall_ij) - 1
    while a < c - 1:
        b = (a + c) // 2
        walls = drop_n_bytes(wall_ij, size, b)
        path = walk(walls)
        if path[-2, -2] == path[0, 0]:  # if the search for a path is unsuccessful
            c = b
        else:
            a = b
    return str(wall_ij[a, 0]) + "," + str(wall_ij[a, 1])


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv
    if argv[0] == "python":
        argv = argv[1:]
    with open(argv[-1]) as hin:
        input_lines = hin.readlines()
    walls = parse(input_lines)
    start = timeit.default_timer()
    if "1" in argv:
        print(solve_1(walls))
    if "2" in argv:
        print(solve_2(walls))

    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

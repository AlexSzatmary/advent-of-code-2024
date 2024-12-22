import numpy as np
import re
import sys
import timeit


def parse(lines: list[str]) -> tuple[np.ndarray, np.ndarray]:
    p = []
    v = []
    for line in lines:
        m = re.match(r"p=(.*),(.*) v=(.*),(.*)", line)
        if m:
            p.append((int(m.group(1)), int(m.group(2))))
            v.append((int(m.group(3)), int(m.group(4))))
    return np.array(p, dtype=int), np.array(v, dtype=int)


def move(
    p: np.ndarray, v: np.ndarray, width: int, height: int, delta_t: int
) -> np.ndarray:
    return (p + v * delta_t) % np.array([width, height])


def count_quadrants(p: np.ndarray, width: int, height: int) -> np.ndarray:
    count = np.zeros(4, dtype=int)
    count[0] = np.sum(np.logical_and(p[:, 0] < width // 2, p[:, 1] < height // 2))
    count[1] = np.sum(np.logical_and(p[:, 0] < width // 2, p[:, 1] > height // 2))
    count[2] = np.sum(np.logical_and(p[:, 0] > width // 2, p[:, 1] < height // 2))
    count[3] = np.sum(np.logical_and(p[:, 0] > width // 2, p[:, 1] > height // 2))
    return count


def solve_1(p: np.ndarray, v: np.ndarray, width: int, height: int, delta_t: int) -> int:
    new_p = move(p, v, width, height, delta_t)
    return np.prod(count_quadrants(new_p, width, height), dtype=int)


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv
    if argv[0] == "python":
        argv = argv[1:]
    with open(argv[-1]) as hin:
        input_lines = hin.readlines()
    p, v = parse(input_lines)
    start = timeit.default_timer()
    if "1" in argv:
        width = np.max(p[:, 0]) + 1
        height = np.max(p[:, 1]) + 1
        delta_t = 100
        print(solve_1(p, v, width, height, delta_t))
    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

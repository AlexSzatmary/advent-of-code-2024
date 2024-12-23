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


def render(p: np.ndarray, width: int, height: int) -> str:
    tiles = np.zeros((height, width), dtype=int)
    for j, i in p:
        tiles[i, j] += 1
    tiles_char = tiles + ord("0")
    tiles_char[tiles_char == ord("0")] = ord(".")
    tiles_char[tiles_char > ord("9")] = ord("X")
    return "\n".join("".join(chr(c) for c in row) for row in tiles_char)


def render_to_int_array(p: np.ndarray, width: int, height: int) -> np.ndarray:
    tiles = np.zeros((height, width), dtype=int)
    for j, i in p:
        tiles[i, j] += 1
    return tiles


def solve_1(p: np.ndarray, v: np.ndarray, width: int, height: int, delta_t: int) -> int:
    new_p = move(p, v, width, height, delta_t)
    return np.prod(count_quadrants(new_p, width, height), dtype=int)


def solve_2(p: np.ndarray, v: np.ndarray, width: int, height: int) -> int:
    height_remainder = 0
    unique_i_min = width * height
    for i in range(height):
        new_p = move(p, v, width, height, i)
        unique_i = np.unique(new_p[:, 1]).size
        if unique_i < unique_i_min:
            height_remainder = i
            unique_i_min = unique_i

    width_remainder = 0
    unique_j_min = width * height
    for j in range(height):
        new_p = move(p, v, width, height, j)
        unique_j = np.unique(new_p[:, 0]).size
        if unique_j < unique_j_min:
            width_remainder = j
            unique_j_min = unique_j

    x = height_remainder
    for j in range(height):
        x = height_remainder + j * height
        if x % width == width_remainder:
            break
    return x


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
    if "2" in argv:
        width = np.max(p[:, 0]) + 1
        height = np.max(p[:, 1]) + 1
        print(solve_2(p, v, width, height))

    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

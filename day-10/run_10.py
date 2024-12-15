import numpy as np
import sys
import timeit

Equation = tuple[int, list[int]]


def parse(input_lines: list[str]) -> np.ndarray:
    topo_map = -np.ones(
        (len(input_lines) + 2, len(input_lines[0]) - 1 + 2), dtype=np.int_
    )
    for i, line in enumerate(input_lines, 1):
        topo_map[i, 1:-1] = list(map(int, line[:-1]))
    return topo_map


def flood_fill_at_loc(topo_map: np.ndarray, i: int, j: int) -> int:
    edges = set()
    edges.add((i, j))
    for level in range(1, 10):
        next_edges = set()
        for edge in edges:
            for didj in np.array([[1, 0], [0, 1], [-1, 0], [0, -1]]):
                new_i, new_j = edge + didj
                if topo_map[new_i, new_j] == level:
                    next_edges.add((new_i, new_j))
        if not next_edges:
            return 0
        edges = next_edges
    return len(next_edges)


def solve_1(topo_map: np.ndarray) -> int:
    count = 0
    for i in range(1, topo_map.shape[0] - 1):
        for j in range(1, topo_map.shape[1] - 1):
            if topo_map[i, j] == 0:
                count += flood_fill_at_loc(topo_map, i, j)
    return count


def move_files_2(
    file_sizes: list[int], gap_sizes: list[int]
) -> list[tuple[int, int, int]]:
    files = []
    files.append((0, file_sizes[0], 0))  # position, size, index
    for index, (gap_size, file_size) in enumerate(zip(gap_sizes, file_sizes[1:]), 1):
        files.append((files[-1][0] + files[-1][1] + gap_size, file_size, index))
    moved_files = files.copy()
    for file in reversed(files):
        for i in range(len(moved_files) - 1):
            if moved_files[i][2] == file[2]:
                break  # found self
            elif (
                moved_files[i + 1][0] - (moved_files[i][0] + moved_files[i][1])
                >= file[1]
            ):
                moved_files.remove(file)
                new_file = ((moved_files[i][0] + moved_files[i][1]), file[1], file[2])
                moved_files.insert(i + 1, new_file)
                break
    return moved_files


def solve_2(blocks: list[int], gaps: list[int]) -> int:
    moved_blocks = move_files_2(blocks, gaps)
    count = 0
    for position, size, index in moved_blocks:
        count += size * (position + position + size - 1) // 2 * index
    return count


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv
    if argv[0] == "python":
        argv = argv[1:]
    with open(argv[-1]) as hin:
        input_lines = hin.readlines()
    topo_map = parse(input_lines)
    start = timeit.default_timer()
    if "1" in argv:
        print(solve_1(topo_map))
    # if "2" in argv:
    #     print(solve_2(blocks, gaps))
    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

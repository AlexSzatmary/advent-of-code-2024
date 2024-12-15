from collections import defaultdict
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


def flood_fill_topo_map(
    topo_map: np.ndarray, start_edges: list[tuple[int, int]]
) -> int:
    edges = defaultdict.fromkeys(start_edges, 1)
    # defaultdict used in initializer for consistency
    for level in range(1, 10):
        next_edges = defaultdict(lambda: 0)
        for edge, weight in edges.items():
            for didj in np.array([[1, 0], [0, 1], [-1, 0], [0, -1]]):
                new_i, new_j = edge + didj
                if topo_map[new_i, new_j] == level:
                    next_edges[new_i, new_j] += weight
        if not next_edges:
            return 0
        edges = next_edges
    return sum(next_edges.values())


def solve_2(topo_map: np.ndarray) -> int:
    start_edges = []
    for i in range(1, topo_map.shape[0] - 1):
        for j in range(1, topo_map.shape[1] - 1):
            if topo_map[i, j] == 0:
                start_edges.append((i, j))
    return flood_fill_topo_map(topo_map, start_edges)


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
    if "2" in argv:
        print(solve_2(topo_map))
    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

from collections import defaultdict
import numpy as np
import sys
import timeit

Equation = tuple[int, list[int]]


def parse(L: list[str]) -> np.ndarray:
    garden = np.zeros((len(L) + 2, len(L[0]) - 1 + 2), dtype=int)
    garden[1:-1, 1:-1] = np.array([[ord(c) for c in s[:-1]] for s in L])
    return garden


def array_to_str(array: np.ndarray) -> str:
    """
    Converts array of ints to a string representation
    """
    return "\n".join(
        "".join([chr(c) if c != 0 else "." for c in row[1:-1]]) for row in array[1:-1]
    )


def garden_fill(garden: np.ndarray, i: int, j: int) -> tuple[np.ndarray, int, int, int]:
    """
    Fills part of garden having single continuous plant type.

    Parameters
    ----------
    garden : array with ints representing plant type. This gets modified.
    i : int index of row
    j : int index of column
    n_side : number of sides of the plot

    Returns
    -------
    garden : garden with consumed plants turned to 0
    area : area of filled plot
    perimeter : perimeter of filled plot
    """
    starting_type = garden[i, j]
    region = np.zeros(garden.shape, dtype=np.bool)
    region[i, j] = True
    edges = [(i, j)]
    area = 1  # the starting square area
    perimeter = 0
    n_side = 0
    i_min = i
    i_max = i
    j_min = j
    j_max = j
    while edges:
        next_edges = []
        for edge in edges:
            for didj in np.array([[1, 0], [0, 1], [-1, 0], [0, -1]]):
                new_i, new_j = edge + didj
                if region[new_i, new_j]:
                    pass  # already checked and included
                elif garden[new_i, new_j] == starting_type:
                    next_edges.append((new_i, new_j))
                    region[new_i, new_j] = True
                    i_min = min(i_min, new_i)
                    i_max = max(i_max, new_i)
                    j_min = min(j_min, new_j)
                    j_max = max(j_max, new_j)
                    area += 1
                else:
                    perimeter += 1

        edges = next_edges

    for i in range(i_min - 1, i_max + 1):
        for j in range(j_min - 1, j_max + 1):
            plots_filled = np.sum(region[i : i + 2, j : j + 2])
            if plots_filled == 1 or plots_filled == 3:
                n_side += 1
            elif plots_filled == 2 and region[i, j] == region[i + 1, j + 1]:
                n_side += 2

    garden[region] = 0
    return garden, area, perimeter, n_side


def tally_costs_1(garden: np.ndarray) -> dict[str, int]:
    costs = defaultdict(lambda: 0)
    "Given garden, find costs per region"
    for i in range(1, garden.shape[0] - 1):
        for j in range(1, garden.shape[1] - 1):
            if garden[i, j]:
                starting_type = chr(garden[i, j])
                garden, area, perimeter, _ = garden_fill(garden, i, j)
                costs[starting_type] += area * perimeter
    return costs


def tally_costs_2(garden: np.ndarray) -> dict[str, int]:
    costs = defaultdict(lambda: 0)
    "Given garden, find costs per region"
    for i in range(1, garden.shape[0] - 1):
        for j in range(1, garden.shape[1] - 1):
            if garden[i, j]:
                starting_type = chr(garden[i, j])
                garden, area, _, n_side = garden_fill(garden, i, j)
                costs[starting_type] += area * n_side
    return costs


def solve_1(garden: np.ndarray) -> int:
    return sum(tally_costs_1(garden).values())


def solve_2(garden: np.ndarray) -> int:
    return sum(tally_costs_2(garden).values())


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv
    if argv[0] == "python":
        argv = argv[1:]
    with open(argv[-1]) as hin:
        input_lines = hin.readlines()
    stones = parse(input_lines)
    start = timeit.default_timer()
    if "1" in argv:
        print(solve_1(stones))
    if "2" in argv:
        print(solve_2(stones))
    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

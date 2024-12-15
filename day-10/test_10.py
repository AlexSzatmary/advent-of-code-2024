import numpy as np
import os
import pytest
from run_10 import parse, flood_fill_at_loc, solve_1


@pytest.fixture
def setup() -> np.ndarray:
    inex_path = os.path.join(os.path.dirname(__file__), "inex-10-1.txt")
    with open(inex_path) as hin:
        inex_1 = hin.readlines()
    return parse(inex_1)


def test_parse(setup: np.ndarray) -> None:
    inex_path = os.path.join(os.path.dirname(__file__), "inex-10-1.txt")
    with open(inex_path) as hin:
        inex_1 = hin.readlines()

    topo_map = setup
    re_stringed = "\n".join(
        "".join(str(x) for x in row) for row in topo_map[1:-1, 1:-1]
    )
    assert re_stringed == "".join(inex_1)[:-1]  # omit trailing newline


def test_flood_fill_at_loc(setup: np.ndarray) -> None:
    topo_map = setup
    ref_it = iter([5, 6, 5, 3, 1, 3, 5, 3, 5])
    for i in range(1, topo_map.shape[0] - 1):
        for j in range(1, topo_map.shape[1] - 1):
            if topo_map[i, j] == 0:
                assert flood_fill_at_loc(topo_map, i, j) == next(ref_it)


def test_solve_1(setup: np.ndarray) -> None:
    assert solve_1(setup) == 36

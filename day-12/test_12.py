from collections import defaultdict
import numpy as np
import os
import pytest
from run_12 import parse, garden_fill, tally_costs_1, solve_1, array_to_str, solve_2


def load(file_name: str) -> list[str]:
    inex_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(inex_path) as hin:
        lines = hin.readlines()
    return lines


@pytest.fixture
def garden_1() -> np.ndarray:
    return parse(load("inex-12-1.txt"))


@pytest.fixture
def garden_2() -> np.ndarray:
    return parse(load("inex-12-2.txt"))


@pytest.fixture
def garden_3() -> np.ndarray:
    return parse(load("inex-12-3.txt"))


@pytest.fixture
def garden_4() -> np.ndarray:
    return parse(load("inex-12-4.txt"))


@pytest.fixture
def garden_5() -> np.ndarray:
    return parse(load("inex-12-5.txt"))


def test_parse(
    garden_1: np.ndarray, garden_2: np.ndarray, garden_3: np.ndarray
) -> None:
    assert array_to_str(garden_1) == "".join(load("inex-12-1.txt"))[:-1]
    assert array_to_str(garden_2) == "".join(load("inex-12-2.txt"))[:-1]
    assert array_to_str(garden_3) == "".join(load("inex-12-3.txt"))[:-1]


def test_garden_fill(
    garden_1: np.ndarray, garden_2: np.ndarray, garden_4: np.ndarray
) -> None:
    garden = garden_1
    # A
    garden, area, perimeter, n_side = garden_fill(garden, 1, 2)
    print(array_to_str(garden))
    assert np.all(garden[1, 1:-1] == 0)
    assert np.all(garden[2:] == garden_1[2:])
    assert area == 4
    assert perimeter == 10
    assert n_side == 4
    # B
    garden, area, perimeter, n_side = garden_fill(garden, 2, 2)
    assert area == 4
    assert perimeter == 8
    assert n_side == 4
    # C
    garden, area, perimeter, n_side = garden_fill(garden, 3, 4)
    assert area == 4
    assert perimeter == 10
    assert n_side == 8
    # D
    garden, area, perimeter, n_side = garden_fill(garden, 2, 4)
    assert area == 1
    assert perimeter == 4
    assert n_side == 4
    # E
    garden, area, perimeter, n_side = garden_fill(garden, 4, 3)
    assert area == 3
    assert perimeter == 8
    assert n_side == 4

    _, area, perimeter, _ = garden_fill(garden_2, 1, 2)
    assert area == 21
    assert perimeter == 36

    _, area, _, n_side = garden_fill(garden_4, 1, 1)
    assert area == 17
    assert n_side == 12


def test_tally_costs_1(
    garden_1: np.ndarray, garden_2: np.ndarray, garden_3: np.ndarray
) -> None:
    costs_1 = tally_costs_1(garden_1)
    assert [costs_1[c] for c in "ABCDE"] == [40, 32, 40, 4, 24]
    costs_3 = tally_costs_1(garden_3)
    reference = [216, 32, 392, 180, 260, 220, 4, 234, 308, 60, 24]
    assert sum(costs_3.values()) == sum(reference)
    print(costs_3)
    costs_3_ref = defaultdict(lambda: 0)
    for garden_type, cost in zip("RICFVJCEIMS", reference):
        costs_3_ref[garden_type] += cost
    assert costs_3 == costs_3_ref


def test_solve_1(
    garden_1: np.ndarray, garden_2: np.ndarray, garden_3: np.ndarray
) -> None:
    assert solve_1(garden_1) == 140
    assert solve_1(garden_2) == 772
    assert solve_1(garden_3) == 1930


def test_solve_2(
    garden_1: np.ndarray,
    garden_2: np.ndarray,
    garden_3: np.ndarray,
    garden_4: np.ndarray,
    garden_5: np.ndarray,
) -> None:
    assert solve_2(garden_1) == 80
    assert solve_2(garden_2) == 436
    assert solve_2(garden_3) == 1206
    assert solve_2(garden_4) == 236
    assert solve_2(garden_5) == 368

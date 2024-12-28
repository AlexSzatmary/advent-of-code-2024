import numpy as np
import os
import pytest
from run_18 import (
    parse_1,
    solve_1,
)


def load(file_name: str) -> list[str]:
    inex_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(inex_path) as hin:
        lines = hin.readlines()
    return lines


@pytest.fixture
def walls_1() -> np.ndarray:
    return parse_1(load("inex-18-1.txt"))


def test_parse_1(walls_1: np.ndarray) -> None:
    walls = walls_1
    assert walls.shape == (9, 9)
    print("\n".join("".join("#" if c else "." for c in row) for row in walls))
    assert np.sum(walls[1:-1, 1:-1]) == 12


def test_solve_1(walls_1: np.ndarray) -> None:
    walls = walls_1
    assert solve_1(walls) == 22

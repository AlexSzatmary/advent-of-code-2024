import numpy as np
import os
import pytest
from run_18 import (
    parse,
    drop_n_bytes,
    walk,
    solve_1,
    solve_2,
    render_walls_path,
)


def load(file_name: str) -> list[str]:
    inex_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(inex_path) as hin:
        lines = hin.readlines()
    return lines


@pytest.fixture
def wall_ij_1() -> np.ndarray:
    return parse(load("inex-18-1.txt"))


@pytest.fixture
def wall_ij_me() -> np.ndarray:
    return parse(load("inme-18.txt"))


def test_parse(wall_ij_1: np.ndarray) -> None:
    wall_ij = wall_ij_1
    walls = drop_n_bytes(wall_ij, 9, 12)
    assert walls.shape == (9, 9)
    print("\n".join("".join("#" if c else "." for c in row) for row in walls))
    assert np.sum(walls[1:-1, 1:-1]) == 12


def test_solve_1(wall_ij_1: np.ndarray) -> None:
    wall_ij = wall_ij_1
    assert solve_1(wall_ij) == 22


def test_solve_2(wall_ij_1: np.ndarray) -> None:
    wall_ij = wall_ij_1
    assert solve_2(wall_ij) == "6,1"


def test_get_full_coverage(wall_ij_1: np.ndarray, wall_ij_me: np.ndarray) -> None:
    solve_2(wall_ij_me)
    walls = drop_n_bytes(wall_ij_1, 9, 12)
    path = walk(walls)
    render_walls_path(walls, path)

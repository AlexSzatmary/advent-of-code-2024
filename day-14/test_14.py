import numpy as np
import os
import pytest
from run_14 import parse, move, count_quadrants, solve_1


def load(file_name: str) -> list[str]:
    inex_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(inex_path) as hin:
        lines = hin.readlines()
    return lines


@pytest.fixture
def pv_1() -> tuple[np.ndarray, np.ndarray]:
    return parse(load("inex-14-1.txt"))


def test_parse(pv_1: tuple[np.ndarray, np.ndarray]) -> None:
    p_1, v_1 = pv_1
    assert np.all(p_1.shape == (12, 2)) and np.all(v_1.shape == (12, 2))
    assert np.all(p_1[-1] == [9, 5])
    assert np.all(v_1[-1] == [-3, -3])


def test_move(pv_1: tuple[np.ndarray, np.ndarray]) -> None:
    p = np.array([[2, 4]])
    v = np.array([[2, -3]])
    width = 11
    height = 7

    # the following are x, y coordinates
    references = [(2, 4), (4, 1), (6, 5), (8, 2), (10, 6), (1, 3)]
    for i, reference in enumerate(references):
        new_p = move(p, v, width, height, i)
        assert new_p[0, 0] == reference[0]
        assert new_p[0, 1] == reference[1]


def test_count_quadrants(pv_1: tuple[np.ndarray, np.ndarray]) -> None:
    p_1, v_1 = pv_1
    width = np.max(p_1[:, 0]) + 1
    height = np.max(p_1[:, 1]) + 1
    new_p = move(p_1, v_1, width, height, 100)
    print(p_1)
    print(v_1)
    print(new_p)
    assert all(count_quadrants(new_p, width, height) == (1, 4, 3, 1))


def test_solve_1(pv_1: tuple[np.ndarray, np.ndarray]) -> None:
    p_1, v_1 = pv_1
    width = np.max(p_1[:, 0]) + 1
    height = np.max(p_1[:, 1]) + 1
    assert solve_1(p_1, v_1, width, height, 100) == 12

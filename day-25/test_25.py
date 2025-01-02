import numpy as np
import os
import pytest
from run_25 import (
    parse,
    solve_1,
)


def load(file_name: str) -> list[str]:
    inex_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(inex_path) as hin:
        lines = hin.readlines()
    return lines


@pytest.fixture
def locks_keys_1() -> tuple[np.ndarray, np.ndarray]:
    return parse(load("inex-25-1.txt"))


def test_parse(
    locks_keys_1: tuple[np.ndarray, np.ndarray],
) -> None:
    locks, keys = locks_keys_1
    locks_reference = np.array(
        [[int(c) for c in row.split(",")] for row in "0,5,3,4,3\n1,2,0,5,3".split("\n")]
    )
    keys_reference = np.array(
        [
            [int(c) for c in row.split(",")]
            for row in "5,0,2,1,3\n4,3,4,0,2\n3,0,2,0,1".split("\n")
        ]
    )
    assert np.all(locks == locks_reference)
    assert np.all(keys == keys_reference)


def test_solve_1(
    locks_keys_1: tuple[np.ndarray, np.ndarray],
) -> None:
    locks, keys = locks_keys_1
    assert solve_1(locks, keys) == 3

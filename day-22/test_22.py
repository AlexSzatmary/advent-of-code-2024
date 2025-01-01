from itertools import pairwise
import os
import pytest
from run_22 import (
    parse,
    find_next_secret_number,
    find_nth_secret_number,
    solve_1,
)


def load(file_name: str) -> list[str]:
    inex_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(inex_path) as hin:
        lines = hin.readlines()
    return lines


@pytest.fixture
def secret_numbers_1() -> list[int]:
    return parse(load("inex-22-1.txt"))


def test_parse(secret_numbers_1: list[int]) -> None:
    secret_numbers = secret_numbers_1
    assert len(secret_numbers) == 4
    assert secret_numbers[-1] == 2024


def test_find_next_secret_number(secret_numbers_1: list[int]) -> None:
    secret_numbers = [
        123,
        15887950,
        16495136,
        527345,
        704524,
        1553684,
        12683156,
        11100544,
        12249484,
        7753432,
        5908254,
    ]
    for na, nb in pairwise(secret_numbers):
        assert find_next_secret_number(na) == nb


def test_find_nth_secret_number(secret_numbers_1: list[int]) -> None:
    secret_numbers = secret_numbers_1
    references = [
        8685429,
        4700978,
        15273692,
        8667524,
    ]
    nth = 2000
    for secret_number, reference in zip(secret_numbers, references):
        assert find_nth_secret_number(secret_number, nth) == reference


def test_solve_1(secret_numbers_1: list[int]) -> None:
    secret_numbers = secret_numbers_1
    assert solve_1(secret_numbers) == 37327623

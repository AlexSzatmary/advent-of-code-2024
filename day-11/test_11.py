import os
import pytest
from run_11 import parse, blink, solve_1, blink_memo, solve_2


@pytest.fixture
def setup() -> list[int]:
    inex_path = os.path.join(os.path.dirname(__file__), "inex-11-1.txt")
    with open(inex_path) as hin:
        inex_1 = hin.readlines()
    return parse(inex_1)


def test_parse(setup: list[int]) -> None:
    stones = setup
    assert stones == [0, 1, 10, 99, 999]


def test_blink(setup: list[int]) -> None:
    stones = setup
    assert blink(stones) == [1, 2024, 1, 0, 9, 9, 2021976]

    # second example
    stones = [125, 17]
    stones = blink(stones)
    assert stones == [253000, 1, 7]
    for _ in range(5):
        stones = blink(stones)
    assert stones == list(
        map(
            int,
            ("2097446912 14168 4048 2 0 2 4 40 48 2024 40 48 80 96 2 8 6 "
            "7 6 0 3 2").split(),
        )
    )


def test_solve_1(setup: list[int]) -> None:
    assert solve_1([125, 17]) == 55312


def test_blink_memo(setup: list[int]) -> None:
    stones = [125, 17]
    assert sum(blink_memo(stone, 25) for stone in stones) == 55312


def test_solve_2(setup: list[int]) -> None:
    assert solve_2([125, 17])
    assert solve_2(setup) == 149161030616311

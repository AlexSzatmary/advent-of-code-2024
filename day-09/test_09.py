import pytest
from run_09 import parse, move_files, solve_1
import os


@pytest.fixture
def setup() -> tuple[list[int], list[int]]:
    inex_path = os.path.join(os.path.dirname(__file__), "inex-09-1.txt")
    with open(inex_path) as hin:
        inex_1 = hin.readlines()
    return parse(inex_1)


def test_parse(setup: tuple[list[int], list[int]]) -> None:
    blocks, gaps = setup
    chars = [
        str(i) * b + "." * g for i, (b, g) in enumerate(zip(blocks, gaps))
    ]
    chars.append(str(len(blocks) - 1) * blocks[-1])
    assert "".join(chars) == "00...111...2...333.44.5555.6666.777.888899"


def test_move_files(setup: tuple[list[int], list[int]]) -> None:
    assert (
        "".join(map(str, move_files(*setup)))
        == "0099811188827773336446555566"
    )


def test_solve_1(setup: tuple[list[int], list[int]]) -> None:
    assert solve_1(*setup) == 1928

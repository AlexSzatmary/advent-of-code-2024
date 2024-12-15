import pytest
from run_09 import parse, move_files_1, solve_1, move_files_2, solve_2
import os


@pytest.fixture
def setup() -> tuple[list[int], list[int]]:
    inex_path = os.path.join(os.path.dirname(__file__), "inex-09-1.txt")
    with open(inex_path) as hin:
        inex_1 = hin.readlines()
    return parse(inex_1)


def test_parse(setup: tuple[list[int], list[int]]) -> None:
    blocks, gaps = setup
    chars = [str(i) * b + "." * g for i, (b, g) in enumerate(zip(blocks, gaps))]
    chars.append(str(len(blocks) - 1) * blocks[-1])
    assert "".join(chars) == "00...111...2...333.44.5555.6666.777.888899"


def test_move_files_1(setup: tuple[list[int], list[int]]) -> None:
    assert "".join(map(str, move_files_1(*setup))) == "0099811188827773336446555566"


def test_solve_1(setup: tuple[list[int], list[int]]) -> None:
    assert solve_1(*setup) == 1928


def test_move_files_2(setup: tuple[list[int], list[int]]) -> None:
    moved_files = move_files_2(*setup)
    rendered_blocks = []
    for i in range(0, len(moved_files) - 1):
        rendered_blocks.append(str(moved_files[i][2]) * moved_files[i][1])
        rendered_blocks.append(
            "." * (moved_files[i + 1][0] - (moved_files[i][0] + moved_files[i][1]))
        )
    rendered_blocks.append(str(moved_files[-1][2]) * moved_files[-1][1])
    rendered_blocks.append("..")
    assert "".join(
        rendered_blocks
    ) == "00992111777.44.333....5555.6666.....8888.."


def test_solve_2(setup: tuple[list[int], list[int]]) -> None:
    assert solve_2(*setup) == 2858

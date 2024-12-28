import os
import pytest
from run_17 import (
    parse,
    solve_1,
)


def load(file_name: str) -> list[str]:
    inex_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(inex_path) as hin:
        lines = hin.readlines()
    return lines


@pytest.fixture
def program_1() -> tuple[int, int, int, list[int]]:
    return parse(load("inex-17-1.txt"))


def test_parse(program_1: tuple[int, int, int, list[int]]) -> None:
    reg_A, reg_B, reg_C, program = program_1
    assert reg_A == 729
    assert reg_B == 0
    assert reg_C == 0
    assert ",".join(map(str, program)) == "0,1,5,4,3,0"


def test_solve_1(program_1: tuple[int, int, int, list[int]]) -> None:
    reg_A, reg_B, reg_C, program = program_1
    assert solve_1(reg_A, reg_B, reg_C, program) == "4,6,3,5,6,3,5,2,1,0"

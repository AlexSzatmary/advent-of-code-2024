import os
import pytest
from run_17 import (
    parse,
    solve_1,
    interpret,
    solve_2,
)


def load(file_name: str) -> list[str]:
    inex_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(inex_path) as hin:
        lines = hin.readlines()
    return lines


@pytest.fixture
def program_1() -> tuple[int, int, int, list[int]]:
    return parse(load("inex-17-1.txt"))


@pytest.fixture
def program_2() -> tuple[int, int, int, list[int]]:
    return parse(load("inex-17-2.txt"))


def test_parse(program_1: tuple[int, int, int, list[int]]) -> None:
    reg_A, reg_B, reg_C, program = program_1
    assert reg_A == 729
    assert reg_B == 0
    assert reg_C == 0
    assert ",".join(map(str, program)) == "0,1,5,4,3,0"


def test_solve_1(program_1: tuple[int, int, int, list[int]]) -> None:
    reg_A, reg_B, reg_C, program = program_1
    assert solve_1(reg_A, reg_B, reg_C, program) == "4,6,3,5,6,3,5,2,1,0"


def test_solve_2(program_2: tuple[int, int, int, list[int]]) -> None:
    _reg_A, reg_B, reg_C, program = program_2
    assert solve_2(reg_B, reg_C, program) == 117440


def test_all_opcodes() -> None:
    assert interpret(4, 0, 0, [6, 1, 5, 5]) == [2]
    assert interpret(4, 0, 0, [7, 1, 5, 6]) == [2]
    with pytest.raises(ValueError):
        interpret(4, 0, 0, [6, 7])
    assert interpret(0, 3, 0, [1, 7, 5, 5]) == [4]
    assert interpret(0, 3, 7, [4, 0, 5, 5]) == [4]
    assert interpret(25, 0, 0, [2, 4, 5, 5]) == [1]

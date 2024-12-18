import os
import pytest
from run_13 import parse, ClawMachine, n_token_1, solve_1, n_token_2, solve_2


def load(file_name: str) -> list[str]:
    inex_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(inex_path) as hin:
        lines = hin.readlines()
    return lines


@pytest.fixture
def arcade_1() -> list[ClawMachine]:
    return parse(load("inex-13-1.txt"))


def test_parse(arcade_1: list[ClawMachine]) -> None:
    assert arcade_1[-1] == ClawMachine(ax=69, ay=23, bx=27, by=71, px=18641, py=10279)


def test_n_token_1(arcade_1: list[ClawMachine]) -> None:
    references = [280, 0, 200, 0]
    for claw_machine, reference in zip(arcade_1, references):
        assert n_token_1(claw_machine) == reference


def test_n_token_2(arcade_1: list[ClawMachine]) -> None:
    is_nonzeros = [False, True, False, True]
    for claw_machine, is_nonzero in zip(arcade_1, is_nonzeros):
        assert (n_token_2(claw_machine) != 0) == is_nonzero


def test_solve_1(arcade_1: list[ClawMachine]) -> None:
    assert solve_1(arcade_1) == 480


def test_solve_2(arcade_1: list[ClawMachine]) -> None:
    # This reference is pegged to what I found when I solved the example.
    assert solve_2(arcade_1) == 875318608908

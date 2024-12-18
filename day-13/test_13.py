import os
import pytest
from run_13 import parse, ClawMachine, n_token, solve_1


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


def test_n_token(arcade_1: list[ClawMachine]) -> None:
    references = [280, 0, 200, 0]
    for claw_machine, reference in zip(arcade_1, references):
        assert n_token(claw_machine) == reference


def test_solve_1(arcade_1: list[ClawMachine]) -> None:
    assert solve_1(arcade_1) == 480

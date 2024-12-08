import run_03_2
import os

inex_path = os.path.join(os.path.dirname(__file__), "inex-03-2.txt")
with open(inex_path) as hin:
    inex_1 = hin.readlines()
program_1 = inex_1[0]


def test_solve() -> None:
    assert run_03_2.solve(program_1) == 48


def test_solve_without_re() -> None:
    assert run_03_2.solve_without_re(program_1) == 48

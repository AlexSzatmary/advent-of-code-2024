import run_03_1
import os

inex_path = os.path.join(os.path.dirname(__file__), "inex-03-1.txt")
with open(inex_path) as hin:
    inex_1 = hin.readlines()
program_1 = inex_1[0]


def test_solve():
    assert run_03_1.solve(program_1) == 161

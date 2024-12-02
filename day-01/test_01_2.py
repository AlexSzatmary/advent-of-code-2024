import run_01_2
import os

inex_path = os.path.join(os.path.dirname(__file__), "inex-01-1.txt")
with open(inex_path) as hin:
    inex_01 = hin.readlines()


def test_parse():
    L_left, L_right = run_01_2.parse(inex_01)
    assert len(L_left) == len(L_right)


def test_solve():
    left, right = run_01_2.parse(inex_01)
    assert run_01_2.solve(left, right) == 31

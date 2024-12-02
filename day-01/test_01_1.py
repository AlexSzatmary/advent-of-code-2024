import run_01_1
from itertools import pairwise
import os

inex_path = os.path.join(os.path.dirname(__file__), "inex-01-1.txt")
with open(inex_path) as hin:
    inex_01 = hin.readlines()

def test_parse():
    L_left, L_right = run_01_1.parse(inex_01)
    assert len(L_left) == len(L_right)
    for L in [L_left, L_right]:
        assert all([a <= b for a, b in pairwise(L)])

def test_solve():
    L_left, L_right = run_01_1.parse(inex_01)
    assert run_01_1.solve(L_left, L_right) == 11

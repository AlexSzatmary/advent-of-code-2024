from run_06 import parse, solve_1, solve_2
import numpy as np
import os

inex_path = os.path.join(os.path.dirname(__file__), "inex-06-1.txt")
with open(inex_path) as hin:
    inex_1 = hin.readlines()


def test_parse() -> None:
    obstacles, (start_i, start_j) = parse(inex_1)
    assert np.shape(obstacles) == (10, 10)
    assert np.sum(obstacles) == 8
    assert start_i == 6
    assert start_j == 4


def test_solve_1() -> None:
    obstacles, (start_i, start_j) = parse(inex_1)
    assert solve_1(obstacles, (start_i, start_j)) == 41


def test_solve_2() -> None:
    obstacles, (start_i, start_j) = parse(inex_1)
    assert solve_2(obstacles, (start_i, start_j)) == 6

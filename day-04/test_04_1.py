import numpy as np
import run_04_1
import os

inex_path = os.path.join(os.path.dirname(__file__), "inex-04-1.txt")
with open(inex_path) as hin:
    inex_1 = hin.readlines()


def test_parse():
    word_search = run_04_1.parse(inex_1)
    assert np.size(word_search, 0) == len(inex_1)
    assert np.size(word_search, 1) == len(inex_1[0]) - 1


def test_crossword_to_str():
    word_search = run_04_1.parse(inex_1)
    s = run_04_1.crossword_to_str(word_search)
    assert all(
        input_line[:-1] == printed_line
        for input_line, printed_line in zip(inex_1, s.split("\n"))
    )


def test_solve():
    word_search = run_04_1.parse(inex_1)
    assert run_04_1.solve(word_search) == 18

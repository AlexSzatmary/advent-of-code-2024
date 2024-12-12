from run_07 import parse, is_possible, solve_1, is_possible_2, solve_2
import os

inex_path = os.path.join(os.path.dirname(__file__), "inex-07-1.txt")
with open(inex_path) as hin:
    inex_1 = hin.readlines()


def test_parse() -> None:
    equations = parse(inex_1)
    assert len(equations) == 9
    test_value, terms = equations[-1]
    assert test_value == 292
    assert terms == [11, 6, 16, 20]


def test_is_possible() -> None:
    equations = parse(inex_1)
    references = [True, True, False, False, False, False, False, False, True]
    for equation, reference in zip(equations, references):
        test_value, terms = equation
        assert is_possible(test_value, 0, terms) == reference
    assert not is_possible(1, 1, [1, 2, 1])


def test_solve_1() -> None:
    equations = parse(inex_1)
    assert solve_1(equations) == 3749


def test_is_possible_2() -> None:
    equations = parse(inex_1)
    references = [True, True, False, True, True, False, True, False, True]
    for equation, reference in zip(equations, references):
        test_value, terms = equation
        assert is_possible_2(test_value, 0, terms) == reference
    assert not is_possible_2(1, 1, [1, 2, 1])


def test_solve_2() -> None:
    equations = parse(inex_1)
    assert solve_2(equations) == 11387

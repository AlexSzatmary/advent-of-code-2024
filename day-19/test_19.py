import os
import pytest
from run_19 import parse, is_possible, solve_1, count_possibilities, solve_2


def load(file_name: str) -> list[str]:
    inex_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(inex_path) as hin:
        lines = hin.readlines()
    return lines


@pytest.fixture
def towels_patterns_1() -> tuple[list[str], list[str]]:
    return parse(load("inex-19-1.txt"))


def test_parse_1(towels_patterns_1: tuple[list[str], list[str]]) -> None:
    towels, patterns = towels_patterns_1
    assert len(towels) == 8
    assert towels[-1] == "br"
    assert len(patterns) == 8
    assert patterns[-1] == "bbrgwb"


def test_is_possible(towels_patterns_1: tuple[list[str], list[str]]) -> None:
    towels, patterns = towels_patterns_1
    references = [True, True, True, True, False, True, True, False]
    for pattern, reference in zip(patterns, references):
        assert is_possible(towels, pattern) == reference


def test_count_possibilities(towels_patterns_1: tuple[list[str], list[str]]) -> None:
    towels, patterns = towels_patterns_1
    references = [2, 1, 4, 6, 0, 1, 2, 0]
    for pattern, reference in zip(patterns, references):
        assert count_possibilities(towels, pattern) == reference


def test_solve_1(towels_patterns_1: tuple[list[str], list[str]]) -> None:
    towels, patterns = towels_patterns_1
    assert solve_1(towels, patterns) == 6


def test_solve_2(towels_patterns_1: tuple[list[str], list[str]]) -> None:
    towels, patterns = towels_patterns_1
    assert solve_2(towels, patterns) == 16

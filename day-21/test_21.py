from itertools import pairwise
import os
import pytest
from run_21 import (
    parse,
    find_num_pad_sequence,
    find_d_pad_sequence,
    find_my_sequence,
    calculate_complexity,
    apply_num_pad_sequence,
    apply_d_pad_sequence,
    solve_1,
)


def load(file_name: str) -> list[str]:
    inex_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(inex_path) as hin:
        lines = hin.readlines()
    return lines


@pytest.fixture
def codes_1() -> list[str]:
    return parse(load("inex-21-1.txt"))


def test_parse(codes_1: list[str]) -> None:
    codes = codes_1
    assert len(codes) == 5
    assert codes[-1] == "379A"


def test_find_num_pad_sequence() -> None:
    code = "029A"
    code = "A" + code
    references = ["<A", "^A", ">^^A", "vvvA"]
    for (fro, to), reference in zip(pairwise(code), references):
        assert sorted(find_num_pad_sequence(fro, to)) == sorted(reference)


def test_find_d_pad_sequence() -> None:
    code = "029A"
    code = "A" + code
    reference = "v<<A>>^A<A>AvA<^AA>A<vAAA>^A"
    num_pad_seq = "".join(find_num_pad_sequence(fro, to) for fro, to in pairwise(code))
    d_pad_seq = "".join(
        find_d_pad_sequence(fro, to) for fro, to in pairwise("A" + num_pad_seq)
    )
    assert sorted(d_pad_seq) == sorted(reference)


def test_find_my_sequence(codes_1: list[str]) -> None:
    codes = codes_1
    references = [
        "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A",
        "<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A",
        "<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A",
        "<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A",
        "<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A",
    ]
    for code, reference in zip(codes, references):
        # print(find_my_sequence(code))
        print()
        print(reference)
        assert len(find_my_sequence(code)) == len(reference)
        assert (
            apply_num_pad_sequence(
                apply_d_pad_sequence(apply_d_pad_sequence(find_my_sequence(code)))
            )
            == code
        )


def test_calculate_complexity(codes_1: list[str]) -> None:
    codes = codes_1
    assert calculate_complexity(codes[0], find_my_sequence(codes[0])) == 68 * 29


def test_solve_1(codes_1: list[str]) -> None:
    codes = codes_1
    assert solve_1(codes) == 126384


def test_corner_case() -> None:
    assert solve_1(["117A"]) == 7488

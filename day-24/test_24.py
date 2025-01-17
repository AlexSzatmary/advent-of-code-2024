from inspect import cleandoc
import os
import pytest
from run_24 import (
    OP,
    parse,
    evaluate,
    combine_bits,
    solve_1,
    find_swapped_gates_full,
    solve_2,
    get_bit,
)


def load(file_name: str) -> list[str]:
    inex_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(inex_path) as hin:
        lines = hin.readlines()
    return lines


@pytest.fixture
def wires_gates_1() -> tuple[dict[str, bool], dict[str, tuple[str, OP, str]]]:
    return parse(load("inex-24-1.txt"))


@pytest.fixture
def wires_gates_2() -> tuple[dict[str, bool], dict[str, tuple[str, OP, str]]]:
    return parse(load("inex-24-2.txt"))


@pytest.fixture
def wires_gates_me() -> tuple[dict[str, bool], dict[str, tuple[str, OP, str]]]:
    return parse(load("inme-24.txt"))


@pytest.fixture
def evaluated_wires_2() -> dict[str, bool]:
    lines = cleandoc("""
    bfw: 1
    bqk: 1
    djm: 1
    ffh: 0
    fgs: 1
    frj: 1
    fst: 1
    gnj: 1
    hwm: 1
    kjc: 0
    kpj: 1
    kwq: 0
    mjb: 1
    nrd: 1
    ntg: 0
    pbm: 1
    psh: 1
    qhw: 1
    rvg: 0
    tgd: 0
    tnw: 1
    vdt: 1
    wpb: 0
    z00: 0
    z01: 0
    z02: 0
    z03: 1
    z04: 0
    z05: 1
    z06: 1
    z07: 1
    z08: 1
    z09: 1
    z10: 1
    z11: 0
    z12: 0
    """).split("\n")
    evaluated_wires = {line[:3]: bool(int(line[5])) for line in lines}
    return evaluated_wires


def test_parse(
    wires_gates_1: tuple[dict[str, bool], dict[str, tuple[str, OP, str]]],
) -> None:
    wires, gates = wires_gates_1
    assert len(wires) == 6
    assert wires["y02"] is False
    assert len(gates) == 3
    assert gates["z02"] == ("x02", "OR", "y02")


def test_evaluate(
    wires_gates_2: tuple[dict[str, bool], dict[str, tuple[str, OP, str]]],
    evaluated_wires_2: dict[str, bool],
) -> None:
    wires, gates = wires_gates_2
    reference_wires = evaluated_wires_2
    wires = evaluate(wires, gates)
    wires_without_input = {
        k: v for k, v in wires.items() if not (k.startswith("x") or k.startswith("y"))
    }
    assert len(wires_without_input) == len(reference_wires)
    for wire in wires_without_input:
        assert wires[wire] == reference_wires[wire]


def test_combine_bits(
    evaluated_wires_2: dict[str, bool],
) -> None:
    assert combine_bits(evaluated_wires_2) == 2024


def test_solve_1(
    wires_gates_2: tuple[dict[str, bool], dict[str, tuple[str, OP, str]]],
) -> None:
    wires, gates = wires_gates_2
    assert solve_1(wires.copy(), gates) == 2024


def test_find_swapped_gates_full(
    wires_gates_me: tuple[dict[str, bool], dict[str, tuple[str, OP, str]]],
) -> None:
    _wires, gates = wires_gates_me
    _swapped_gates, gates_4 = find_swapped_gates_full(gates)

    # two random integers
    x = 15564911598446
    y = 16228481894866
    wires = {
        **{f"x{i:02}": bool(x & (1 << i)) for i in range(45)},
        **{f"y{i:02}": bool(y & (1 << i)) for i in range(45)},
    }
    assert combine_bits(evaluate(wires, gates_4)) == x + y


def test_solve_2(
    wires_gates_me: tuple[dict[str, bool], dict[str, tuple[str, OP, str]]],
) -> None:
    wires, gates = wires_gates_me
    assert solve_2(wires, gates) == "gsd,kth,qnf,tbt,vpm,z12,z26,z32"


def test_get_bit_raises_error() -> None:
    assert (
        int(
            get_bit(
                {
                    "a": ("b", "XOR", "c"),
                    "b": ("x00", "XOR", "bad"),
                    "c": ("bad", "AND", "bad"),
                },
                "a",
            )
        )
        == 0
    )
    with pytest.raises(ValueError):
        get_bit(
            {
                "a": ("b", "XOR", "c"),
                "b": ("x00", "AND", "bad"),
                "c": ("bad", "AND", "bad"),
            },
            "a",
        )

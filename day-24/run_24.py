import re
import sys
import timeit
from typing import Literal


OP = Literal["AND"] | Literal["OR"] | Literal["XOR"]


def parse(lines: list[str]) -> tuple[dict[str, bool], dict[str, tuple[str, OP, str]]]:
    """
    Given input, creates network

    Parameters
    ----------
    lines : text of input file as list of strings

    Returns
    -------
    wires : key: wire, value: bool
    gates : key: output wire, value: tuple of input0, operator, input1
    """
    wires = {}
    gates = {}
    for line in lines:
        if m := re.match(r"(\w+): (\d)", line):
            wires[m.group(1)] = bool(int(m.group(2)))
        elif m := re.match(r"(\w+) (\w+) (\w+) -> (\w+)", line):
            gates[m.group(4)] = (m.group(1), m.group(2), m.group(3))
    return wires, gates


def operate(input0: bool, op: OP, input1: bool) -> bool:  # noqa: FBT001
    match op:
        case "AND":
            return input0 and input1
        case "OR":
            return input0 or input1
        case "XOR":
            return bool(input0) != bool(input1)


def evaluate(
    wires: dict[str, bool], gates: dict[str, tuple[str, OP, str]]
) -> dict[str, bool]:
    """
    Given input, creates network

    Parameters
    ----------
    wires : key: wire, value: bool
    gates : key: output wire, value: tuple of input0, operator, input1

    Returns
    -------
    wires : same dict as input
    """
    gates_to_evaluate = set(gates) - set(wires)
    while gates_to_evaluate:
        just_evaluated = set()
        for gate in gates_to_evaluate:
            input0, op, input1 = gates[gate]
            if gate not in wires and input0 in wires and input1 in wires:
                wires[gate] = operate(wires[input0], op, wires[input1])
                just_evaluated.add(gate)
        gates_to_evaluate -= just_evaluated
    return wires


def combine_bits(wires: dict[str, bool]) -> int:
    return sum(
        1 << int(wire[1:3]) for wire, val in wires.items() if wire[0] == "z" and val
    )


def solve_1(wires: dict[str, bool], gates: dict[str, tuple[str, OP, str]]) -> int:
    return combine_bits(evaluate(wires, gates))


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv
    if argv[0] == "python":
        argv = argv[1:]
    with open(argv[-1]) as hin:
        input_lines = hin.readlines()
    wires, gates = parse(input_lines)
    start = timeit.default_timer()
    if "1" in argv:
        print(solve_1(wires.copy(), gates))

    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

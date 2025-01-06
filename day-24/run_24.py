import pathlib
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


# an adder step should look like,
# x_n XOR y_n -> a
# a XOR c_n-1 -> z_n
# x_n AND y_n -> b
# a AND c_n-1 -> d
# b OR d -> c_n
# it could be wired up differently but that's the normal way for the input
#
# Things to check for:
# z not tied to XOR
# z on XOR tied to x (and y)
# OR named z
# OR having an input other than an AND gate
# AND named z
# If AND is not on xy, it should be on an XOR on an xy and an OR. If not, one of its
# input gates is miswired and that should be labeled.


def find_bad_z(gates: dict[str, tuple[str, OP, str]]) -> list[str]:
    return [
        gate for gate in gates if (gate.startswith("z") and not gates[gate][1] == "XOR")
    ]


def find_gates_that_should_not_be_z(gates: dict[str, tuple[str, OP, str]]) -> list[str]:
    max_z = max(gates)
    return [
        gate
        for gate in gates
        if gate.startswith("z") and not gates[gate][1] == "XOR" and gate != max_z
    ]


def find_gates_that_should_be_z(gates: dict[str, tuple[str, OP, str]]) -> list[str]:
    # an XOR on an xy can't have its targets miswired
    # so if an XOR doesn't target xy, it must be a z xor
    return [
        gate
        for gate in gates
        if (
            not gate.startswith("z")
            and gates[gate][1] == "XOR"
            and gates[gate][0][0] not in "xy"
        )
    ]


def get_bit(gates: dict[str, tuple[str, OP, str]], gate: str) -> str:
    """
    For an xor known to not have x or y as an input, find the xor it has as an input,
    find an xNN or yNN input to that, and get the NN. For example, find 32 for an
    xor taking an xor taking x32. Outputs as a string, not int.
    """
    i0, _op, i1 = gates[gate]
    target_bit = None
    for i in [i0, i1]:
        # one of i0 or i1 should have an input that looks like 'x32', 'XOR', 'y32'.
        i_0, op, _i_1 = gates[i]
        if op == "XOR":
            target_bit = i_0[1:]
            # pull the "32" from "x32" or "y32", for example.
    if target_bit is None:
        msg = f"Gate {gate} cannot find its bit"
        raise ValueError(msg)
    return target_bit


def find_swapped_gates_full(
    gates: dict[str, tuple[str, OP, str]],
) -> tuple[list[str], dict[str, tuple[str, OP, str]]]:
    gates = gates.copy()
    gates_that_should_not_be_z = find_gates_that_should_not_be_z(gates)
    gates_that_should_be_z = find_gates_that_should_be_z(gates)
    for gate in gates_that_should_be_z:
        target_bit = get_bit(gates, gate)
        gates["z" + target_bit], gates[gate] = gates[gate], gates["z" + target_bit]
    # now 3 of the 4 swaps are healed. I need to find the last swap.
    max_z = max(gates)
    # by inspection, I found one z gate that still did not take an xor that takes xy
    z4 = next(
        gate
        for gate, (i0, op, i1) in gates.items()
        if gate.startswith("z")
        and gate != "z00"
        and gate != max_z
        and gates[i0][1] != "XOR"
        and gates[i1][1] != "XOR"
    )
    weird_and = gates[z4][0] if gates[z4][0][1] == "AND" else gates[z4][2]
    # by inspection, I found one OR that takes an XOR, which z4 should target
    weird_or = next(
        gate
        for gate, (i0, op, i1) in gates.items()
        if op == "OR" and (gates[i0][1] == "XOR" or gates[i1][1] == "XOR")
    )
    weird_xor = (
        gates[weird_or][0] if gates[weird_or][0][1] == "XOR" else gates[weird_or][2]
    )
    gates[weird_xor], gates[weird_and] = gates[weird_and], gates[weird_xor]
    return [
        *gates_that_should_not_be_z,
        *gates_that_should_be_z,
        weird_and,
        weird_xor,
    ], gates


def find_swapped_gates(gates: dict[str, tuple[str, OP, str]]) -> list[str]:
    return find_swapped_gates_full(gates)[0]


def solve_2(_wires: dict[str, bool], gates: dict[str, tuple[str, OP, str]]) -> str:
    return ",".join(sorted(find_swapped_gates(gates)))


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv
    if argv[0] == "python":
        argv = argv[1:]
    with open(argv[-1]) as hin:
        input_lines = hin.readlines()
    wires, gates = parse(input_lines)
    start = timeit.default_timer()
    if "graphviz" in argv:
        with open(pathlib.Path(argv[-1]).stem + ".dot", "w") as hout:
            shapes = {"AND": "box", "OR": "oval", "XOR": "diamond"}
            hout.write("digraph {\n")
            for node, (input0, op, input1) in gates.items():
                hout.write(f"{node} [shape={shapes[op]}]")
                hout.write(f"{input0} -> {node}\n")
                hout.write(f"{input1} -> {node}\n")
            hout.write("}\n")
        # invoke graphviz with, e.g.,
        # dot -Tpng < inme-05.dot>inme-05.png
    if "1" in argv:
        print(solve_1(wires.copy(), gates))
    if "2" in argv:
        print(solve_2(wires, gates))

    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

from run_08 import parse, find_antinodes_1, solve_1, find_antinodes_2, solve_2
import os

inex_path = os.path.join(os.path.dirname(__file__), "inex-08-1.txt")
with open(inex_path) as hin:
    inex_1 = hin.readlines()

inex_path_ref = os.path.join(os.path.dirname(__file__), "inex-08-1-ref.txt")
with open(inex_path_ref) as hin:
    inex_1_ref = hin.readlines()

inex_path_ref = os.path.join(os.path.dirname(__file__), "inex-08-2-ref.txt")
with open(inex_path_ref) as hin:
    inex_2_ref = hin.readlines()


def test_parse() -> None:
    frequencies_antennas = parse(inex_1)
    assert len(frequencies_antennas) == 2
    assert len(frequencies_antennas["0"]) == 4
    assert len(frequencies_antennas["A"]) == 3
    assert (1, 8) in frequencies_antennas["0"]
    for i, line in enumerate(inex_1):
        for j, c in enumerate(line[:-1]):  # strip newline
            if c != ".":
                assert (i, j) in frequencies_antennas[c]


def test_find_antinodes_1() -> None:
    frequencies_antennas = parse(inex_1)
    frequencies_antennas_ref = parse(inex_1_ref)
    antinodes_ref = frequencies_antennas_ref["#"]
    # we can use the parser to get just the # from the ref

    # manually add in antinode at top A:
    antinodes_ref.append(min(frequencies_antennas_ref["A"]))
    # min gives us the right one because the loc tuples are sorted first by i

    antinodes = find_antinodes_1(frequencies_antennas, len(inex_1), len(inex_1[0]) - 1)
    assert len(antinodes) == len(antinodes_ref)
    for antinode in antinodes_ref:
        assert antinode in antinodes


def test_solve_1() -> None:
    frequencies_antennas = parse(inex_1)
    assert solve_1(frequencies_antennas, len(inex_1), len(inex_1[0]) - 1) == 14


def test_find_antinodes_2() -> None:
    frequencies_antennas = parse(inex_1)
    frequencies_antennas_ref = parse(inex_2_ref)
    antinodes_ref = set()
    for v in frequencies_antennas_ref.values():
        antinodes_ref.update(v)
    # mash together the #, A, and 0 marks

    antinodes = find_antinodes_2(frequencies_antennas, len(inex_1), len(inex_1[0]) - 1)
    assert len(antinodes) == len(antinodes_ref)
    for antinode in antinodes_ref:
        assert antinode in antinodes


def test_solve_2() -> None:
    frequencies_antennas = parse(inex_1)
    assert solve_2(frequencies_antennas, len(inex_1), len(inex_1[0]) - 1) == 34

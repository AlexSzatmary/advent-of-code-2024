from collections import defaultdict
import sys
import timeit

Equation = tuple[int, list[int]]


def parse(input_lines: list[str]) -> dict[str, list[tuple[int, int]]]:
    frequencies_antennas = defaultdict(list)
    for i, line in enumerate(input_lines):
        for j, c in enumerate(line[:-1]):  # drop newline
            if c != ".":
                frequencies_antennas[c].append((i, j))
    return frequencies_antennas


def find_antinodes_1(
    frequencies_antennas: dict[str, list[tuple[int, int]]], imax: int, jmax: int
) -> set[tuple[int, int]]:
    antinodes = set()
    for antennas in frequencies_antennas.values():
        for p in range(0, len(antennas) - 1):
            for q in range(p + 1, len(antennas)):
                p_i, p_j = antennas[p]
                q_i, q_j = antennas[q]
                a_i, a_j = 2 * p_i - q_i, 2 * p_j - q_j
                if 0 <= a_i < imax and 0 <= a_j < jmax:
                    antinodes.add((a_i, a_j))
                b_i, b_j = 2 * q_i - p_i, 2 * q_j - p_j
                if 0 <= b_i < imax and 0 <= b_j < jmax:
                    antinodes.add((b_i, b_j))
    return antinodes


def solve_1(
    frequencies_antennas: dict[str, list[tuple[int, int]]], imax: int, jmax: int
) -> int:
    antinodes = find_antinodes_1(frequencies_antennas, imax, jmax)
    return len(antinodes)


def find_antinodes_2(
    frequencies_antennas: dict[str, list[tuple[int, int]]], imax: int, jmax: int
) -> set[tuple[int, int]]:
    antinodes = set()
    for antennas in frequencies_antennas.values():
        antinodes.update(antennas)  # add all antennas, which are now all antinodes
        for p in range(0, len(antennas) - 1):
            for q in range(p + 1, len(antennas)):
                p_i, p_j = antennas[p]
                q_i, q_j = antennas[q]

                k = 1
                while True:
                    a_i, a_j = p_i + k * (p_i - q_i), p_j + k * (p_j - q_j)
                    if 0 <= a_i < imax and 0 <= a_j < jmax:
                        antinodes.add((a_i, a_j))
                    else:
                        break
                    k += 1

                k = 1
                while True:
                    a_i, a_j = p_i - k * (p_i - q_i), p_j - k * (p_j - q_j)
                    if 0 <= a_i < imax and 0 <= a_j < jmax:
                        antinodes.add((a_i, a_j))
                    else:
                        break
                    k += 1
    return antinodes


def solve_2(
    frequencies_antennas: dict[str, list[tuple[int, int]]], imax: int, jmax: int
) -> int:
    antinodes = find_antinodes_2(frequencies_antennas, imax, jmax)
    return len(antinodes)


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv
    if argv[0] == "python":
        argv = argv[1:]
    with open(argv[-1]) as hin:
        input_lines = hin.readlines()
    frequencies_antennas = parse(input_lines)
    start = timeit.default_timer()
    if "1" in argv:
        print(solve_1(frequencies_antennas, len(input_lines), len(input_lines[0]) - 1))
    if "2" in argv:
        print(solve_2(frequencies_antennas, len(input_lines), len(input_lines[0]) - 1))
    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

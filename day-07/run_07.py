import sys
import timeit

Equation = tuple[int, list[int]]


def parse(input_lines: list[str]) -> list[Equation]:
    equations = []
    for line in input_lines:
        items = line[:-1].split()  # [:-1] to remove newline
        equations.append((int(items[0][:-1]), list(map(int, items[1:]))))
    return equations


def is_possible(test_value: int, subtotal: int, terms: list[int]) -> bool:
    if not terms:
        return test_value == subtotal
    elif subtotal > test_value:
        return False
    else:
        return is_possible(test_value, subtotal + terms[0], terms[1:]) or is_possible(
            test_value, subtotal * terms[0], terms[1:]
        )


def solve_1(equations: list[Equation]) -> int:
    return sum(
        test_value
        for test_value, terms in equations
        if is_possible(test_value, 0, terms)
    )


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv
    if argv[0] == "python":
        argv = argv[1:]
    with open(argv[-1]) as hin:
        input_lines = hin.readlines()
    equations = parse(input_lines)
    start = timeit.default_timer()
    if "1" in argv:
        print(solve_1(equations))
    elif "2" in argv:
        pass
    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

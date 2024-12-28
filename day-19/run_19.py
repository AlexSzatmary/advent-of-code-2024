import sys
import timeit


def parse(lines: list[str]) -> tuple[list[str], list[str]]:
    towels = lines[0][:-1].split(", ")
    patterns = [line[:-1] for line in lines[2:]]
    return towels, patterns


def is_possible(towels: list[str], pattern: str) -> int:
    if not pattern:
        return True

    for towel in towels:
        if pattern.startswith(towel) and is_possible(towels, pattern[len(towel):]):
            return True
    return False


def solve_1(towels: list[str], patterns: list[str]) -> int:
    return sum(is_possible(towels, pattern) for pattern in patterns)


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv
    if argv[0] == "python":
        argv = argv[1:]
    with open(argv[-1]) as hin:
        input_lines = hin.readlines()
    towels, patterns = parse(input_lines)
    start = timeit.default_timer()
    if "1" in argv:
        print(solve_1(towels, patterns))

    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

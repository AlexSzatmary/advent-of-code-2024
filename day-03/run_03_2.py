import re
import sys
import timeit
from itertools import starmap


def solve_without_re(program: str) -> int:
    """
    I got this solution first and I still think it's nice.
    """
    dont = 0
    do = 0
    total = 0
    while do != -1:
        dont = program.find("don't()", do)
        total += sum(
            starmap(
                lambda a, b: int(a) * int(b),
                re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", program[do:dont]),
            )
        )
        do = program.find("do()", dont)
    return total


def solve(program: str) -> int:
    program_scrubbed = re.sub("don't.*", "", re.sub(r"don't\(\).*?do\(\)", "", program))
    return sum(
        starmap(
            lambda a, b: int(a) * int(b),
            re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", program_scrubbed),
        )
    )


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv
    if argv[0] == "python":
        argv = argv[1:]
    with open(argv[1]) as hin:
        L = hin.readlines()
    program = "".join(L).replace("\n", "")
    start = timeit.default_timer()
    print(solve(program))
    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

import re
import sys
import timeit
from itertools import starmap


def solve(program: str) -> int:
    return sum(
        starmap(
            lambda a, b: int(a) * int(b),
            re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", program),
        )
    )


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv
    if argv[0] == "python":
        argv = argv[1:]
    with open(argv[1]) as hin:
        L = hin.readlines()
    program = "".join(L)
    start = timeit.default_timer()
    print(solve(program))
    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

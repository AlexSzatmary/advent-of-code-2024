from collections import namedtuple
import re
import sys
import timeit

ClawMachine = namedtuple("ClawMachine", ["ax", "ay", "bx", "by", "px", "py"])


def parse(lines: list[str]) -> list[ClawMachine]:
    s = "".join(lines)
    pattern = r"(?s)X\+(\d+).*?Y\+(\d+).*?X\+(\d+).*?Y\+(\d+).*?X=(\d+).*?Y=(\d+)"
    return [ClawMachine(*map(int, tup)) for tup in re.findall(pattern, s)]


def n_token_1(cm: ClawMachine) -> int:
    det = cm.ax * cm.by - cm.bx * cm.ay
    na = (cm.by * cm.px - cm.bx * cm.py) // det
    nb = (-cm.ay * cm.px + cm.ax * cm.py) // det
    if cm.ax * na + cm.bx * nb == cm.px and cm.ay * na + cm.by * nb == cm.py:
        return 3 * na + nb
    else:
        return 0


def solve_1(arcade: list[ClawMachine]) -> int:
    return sum(map(n_token_1, arcade))


def n_token_2(cm: ClawMachine) -> int:
    cm = cm._replace(px=cm.px + 10000000000000, py=cm.py + 10000000000000)
    det = cm.ax * cm.by - cm.bx * cm.ay
    na = (cm.by * cm.px - cm.bx * cm.py) // det
    nb = (-cm.ay * cm.px + cm.ax * cm.py) // det
    if cm.ax * na + cm.bx * nb == cm.px and cm.ay * na + cm.by * nb == cm.py:
        return 3 * na + nb
    else:
        return 0


def solve_2(arcade: list[ClawMachine]) -> int:
    return sum(map(n_token_2, arcade))


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv
    if argv[0] == "python":
        argv = argv[1:]
    with open(argv[-1]) as hin:
        input_lines = hin.readlines()
    stones = parse(input_lines)
    start = timeit.default_timer()
    if "1" in argv:
        print(solve_1(stones))
    if "2" in argv:
        print(solve_2(stones))
    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

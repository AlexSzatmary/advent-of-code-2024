from itertools import pairwise
import sys
import timeit


def parse(lines: list[str]) -> list[str]:
    return [line[:-1] for line in lines]


NUM_PAD_COORDS = {}
num_pad = "789 456 123 X0A".split()
for i in range(len(num_pad)):
    for j in range(len(num_pad[0])):
        NUM_PAD_COORDS[num_pad[i][j]] = (i, j)

D_PAD_COORDS = {}
d_pad = "X^A <v>".split()
for i in range(len(d_pad)):
    for j in range(len(d_pad[0])):
        D_PAD_COORDS[d_pad[i][j]] = (i, j)


def find_num_pad_sequence(fro: str, to: str) -> str:
    fi, fj = NUM_PAD_COORDS[fro]
    ti, tj = NUM_PAD_COORDS[to]
    if (fi == 3 and tj == 0):  # need to move up first
        horizontal_first = False
    elif (ti == 3 and fj == 0):
        horizontal_first = True
    elif tj > fj:
        horizontal_first = False
    else:
        horizontal_first = True
    if horizontal_first:
        return "".join(
            [">" * (tj - fj), "<" * (fj - tj), "v" * (ti - fi), "^" * (fi - ti), "A"]
        )
    else:
        return "".join(
            ["v" * (ti - fi), "^" * (fi - ti), ">" * (tj - fj), "<" * (fj - tj), "A"]
        )


def find_d_pad_sequence(fro: str, to: str) -> str:
    fi, fj = D_PAD_COORDS[fro]
    ti, tj = D_PAD_COORDS[to]
    if tj == 0 or (tj > fj and ti > fi):  # need to move down first
        return "".join(
            ["v" * (ti - fi), "^" * (fi - ti), ">" * (tj - fj), "<" * (fj - tj), "A"]
        )
    else:
        return "".join(
            [">" * (tj - fj), "<" * (fj - tj), "v" * (ti - fi), "^" * (fi - ti), "A"]
        )


def apply_num_pad_sequence(seq: str) -> str:
    i = 3
    j = 2
    result = []
    for c in seq:
        match c:
            case "A":
                result.append(num_pad[i][j])
            case "v":
                i += 1
            case "^":
                i -= 1
            case "<":
                j -= 1
            case ">":
                j += 1
    return "".join(result)


def apply_d_pad_sequence(seq: str) -> str:
    i = 0
    j = 2
    result = []
    for c in seq:
        match c:
            case "A":
                result.append(d_pad[i][j])
            case "v":
                i += 1
            case "^":
                i -= 1
            case "<":
                j -= 1
            case ">":
                j += 1
    return "".join(result)


def find_my_sequence(code: str) -> str:
    code = "A" + code
    num_pad_seq = "".join(find_num_pad_sequence(fro, to) for fro, to in pairwise(code))
    d_pad_seq = "".join(
        find_d_pad_sequence(fro, to) for fro, to in pairwise("A" + num_pad_seq)
    )
    d_pad_seq = "".join(
        find_d_pad_sequence(fro, to) for fro, to in pairwise("A" + d_pad_seq)
    )
    return d_pad_seq


def calculate_complexity(code: str, sequence: str) -> int:
    return int(code[:-1]) * len(sequence)


def solve_1(codes: list[str]) -> int:
    return sum(calculate_complexity(code, find_my_sequence(code)) for code in codes)


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv
    if argv[0] == "python":
        argv = argv[1:]
    with open(argv[-1]) as hin:
        input_lines = hin.readlines()
    codes = parse(input_lines)
    start = timeit.default_timer()
    if "1" in argv:
        print(solve_1(codes))

    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

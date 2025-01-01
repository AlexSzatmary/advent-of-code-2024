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
    if fi == 3 and tj == 0:  # need to move up first
        horizontal_first = False
    elif ti == 3 and fj == 0:
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
    if tj == 0:  # need to move down first
        horizontal_first = False
    elif fj == 0:  # need to move right first
        horizontal_first = True
    elif tj > fj:  # move vertical first if going right
        horizontal_first = False
    else:  # move left first if going left
        horizontal_first = True
    if horizontal_first:
        return "".join(
            [">" * (tj - fj), "<" * (fj - tj), "v" * (ti - fi), "^" * (fi - ti), "A"]
        )
    else:
        return "".join(
            ["v" * (ti - fi), "^" * (fi - ti), ">" * (tj - fj), "<" * (fj - tj), "A"]
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


def dpad_to_dpad(seq: str) -> str:
    return "".join(find_d_pad_sequence(a, b) for a, b in pairwise("A" + seq))


def find_my_sequence(code: str) -> str:
    return find_my_sequence_n(code, 2)


def find_my_sequence_n(code: str, n_dpad: int) -> str:
    code = "A" + code
    num_pad_seq = "".join(find_num_pad_sequence(fro, to) for fro, to in pairwise(code))
    d_pad_seq = "".join(
        find_d_pad_sequence(fro, to) for fro, to in pairwise("A" + num_pad_seq)
    )
    for _ in range(n_dpad - 1):
        d_pad_seq = "".join(
            find_d_pad_sequence(fro, to) for fro, to in pairwise("A" + d_pad_seq)
        )
    return d_pad_seq


def estimate_length(
    seq: str, n: int, memo: dict[tuple[str, int], int] | None = None
) -> int:
    if memo is None:
        memo = {}
    if n == 0:
        return len(seq)
    if (seq, n) in memo:
        return memo[seq, n]
    result = (
        sum(estimate_length(k + "A", n - 1, memo) for k in dpad_to_dpad(seq).split("A"))
        - 1
    )
    memo[seq, n] = result
    return result


def estimate_code_length(code: str, n_dpad: int) -> int:
    code = "A" + code
    num_pad_seq = "".join(find_num_pad_sequence(fro, to) for fro, to in pairwise(code))
    d_pad_seq = "".join(
        find_d_pad_sequence(fro, to) for fro, to in pairwise("A" + num_pad_seq)
    )
    return estimate_length(d_pad_seq, n_dpad - 1)


def calculate_complexity(code: str, seq_length: int) -> int:
    return int(code[:-1]) * seq_length


def solve_1(codes: list[str]) -> int:
    return sum(
        calculate_complexity(code, estimate_code_length(code, 2)) for code in codes
    )


def solve_2(codes: list[str]) -> int:
    return sum(
        calculate_complexity(code, estimate_code_length(code, 25)) for code in codes
    )


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
    if "2" in argv:
        print(solve_2(codes))

    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

import sys
import timeit
from collections import Counter


def parse(lines: list[str]) -> list[int]:
    return [int(line[:-1]) for line in lines]


def find_next_secret_number(secret_number: int) -> int:
    mod = 16777216
    a = ((secret_number * 64) ^ secret_number) % mod
    b = ((a // 32) ^ a) % mod
    c = ((b * 2048) ^ b) % mod
    return c


def find_nth_secret_number(secret_number: int, nth: int) -> int:
    for _ in range(nth):
        secret_number = find_next_secret_number(secret_number)
    return secret_number


def solve_1(secret_numbers: list[int]) -> int:
    return sum(
        find_nth_secret_number(secret_number, 2000) for secret_number in secret_numbers
    )


def tabulate_combo_bananas(
    secret_numbers: list[int],
) -> Counter[tuple[int, int, int, int]]:
    combo_bananas = Counter()
    for n in secret_numbers:
        lastn = n
        combo = []
        seen_combos = set()
        for _i in range(4):
            nextn = find_next_secret_number(lastn)
            combo.append(nextn % 10 - lastn % 10)
            lastn = nextn
        combo = tuple(combo)
        for _i in range(4, 2000):
            if combo not in seen_combos:
                combo_bananas[combo] += lastn % 10
                seen_combos.add(combo)
            nextn = find_next_secret_number(lastn)
            combo = (combo[1], combo[2], combo[3], nextn % 10 - lastn % 10)
            lastn = nextn
        if combo not in seen_combos:
            combo_bananas[combo] += lastn % 10
            seen_combos.add(combo)
    return combo_bananas


def solve_2(secret_numbers: list[int]) -> int:
    combo_bananas = tabulate_combo_bananas(secret_numbers)
    return combo_bananas.most_common(n=1)[0][1]


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

from functools import cache
import sys
import timeit

Equation = tuple[int, list[int]]


def parse(input_lines: list[str]) -> list[int]:
    return list(map(int, input_lines[0].split()))


def blink(stones: list[int]) -> list[int]:
    new_stones = []
    for stone in stones:
        if stone == 0:
            new_stones.append(1)
        elif len(stone_str := str(stone)) % 2 == 0:
            new_stones.append(int(stone_str[: len(stone_str) // 2]))
            new_stones.append(int(stone_str[len(stone_str) // 2 :]))
        else:
            new_stones.append(stone * 2024)
    return new_stones


@cache
def blink_memo(stone: int, n: int) -> int:
    if n == 0:
        return 1
    if stone == 0:
        return blink_memo(1, n - 1)
    elif len(stone_str := str(stone)) % 2 == 0:
        return blink_memo(int(stone_str[: len(stone_str) // 2]), n - 1) + blink_memo(
            int(stone_str[len(stone_str) // 2 :]), n - 1
        )
    else:
        return blink_memo(stone * 2024, n - 1)


def solve_1(stones: list[int]) -> int:
    return sum(blink_memo(stone, 25) for stone in stones)


def solve_2(stones: list[int]) -> int:
    return sum(blink_memo(stone, 75) for stone in stones)


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

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


def solve_1(stones: list[int]) -> int:
    for _ in range(25):
        stones = blink(stones)
    return len(stones)


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv
    if argv[0] == "python":
        argv = argv[1:]
    with open(argv[-1]) as hin:
        input_lines = hin.readlines()
    topo_map = parse(input_lines)
    start = timeit.default_timer()
    if "1" in argv:
        print(solve_1(topo_map))
    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

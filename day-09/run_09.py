import sys
import timeit
from collections.abc import Generator

Equation = tuple[int, list[int]]


def parse(input_lines: list[str]) -> tuple[list[int], list[int]]:
    return list(map(int, input_lines[0][:-1:2])), list(map(int, input_lines[0][1:-1:2]))


def move_files(block_sizes: list[int], gap_sizes: list[int]) -> Generator[int]:
    right_gen = (
        len(block_sizes) - i - 1
        for i, block_size in enumerate(reversed(block_sizes))
        for _ in range(block_size)
    )
    k = 0
    max_k = sum(block_sizes)
    for block_id, (block_size, gap_size) in enumerate(zip(block_sizes, gap_sizes)):
        for _ in range(block_size):
            k += 1
            if k > max_k:
                break
            yield block_id
        for _ in range(gap_size):
            k += 1
            if k > max_k:
                break
            yield next(right_gen)


def solve_1(blocks: list[int], gaps: list[int]) -> int:
    return sum(i * file_id for i, file_id in enumerate(move_files(blocks, gaps)))


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv
    if argv[0] == "python":
        argv = argv[1:]
    with open(argv[-1]) as hin:
        input_lines = hin.readlines()
    blocks, gaps = parse(input_lines)
    start = timeit.default_timer()
    if "1" in argv:
        print(solve_1(blocks, gaps))
    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

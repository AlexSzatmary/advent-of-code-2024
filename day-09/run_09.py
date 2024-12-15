import sys
import timeit
from collections.abc import Generator

Equation = tuple[int, list[int]]


def parse(input_lines: list[str]) -> tuple[list[int], list[int]]:
    return list(map(int, input_lines[0][:-1:2])), list(map(int, input_lines[0][1:-1:2]))


def move_files_1(file_sizes: list[int], gap_sizes: list[int]) -> Generator[int]:
    right_gen = (
        len(file_sizes) - i - 1
        for i, file_size in enumerate(reversed(file_sizes))
        for _ in range(file_size)
    )
    k = 0
    max_k = sum(file_sizes)
    for file_id, (file_size, gap_size) in enumerate(zip(file_sizes, gap_sizes)):
        for _ in range(file_size):
            k += 1
            if k > max_k:
                break
            yield file_id
        for _ in range(gap_size):
            k += 1
            if k > max_k:
                break
            yield next(right_gen)


def solve_1(file_sizes: list[int], gap_sizes: list[int]) -> int:
    return sum(
        i * file_id for i, file_id in enumerate(move_files_1(file_sizes, gap_sizes))
    )


def move_files_2(
    file_sizes: list[int], gap_sizes: list[int]
) -> list[tuple[int, int, int]]:
    files = []
    files.append((0, file_sizes[0], 0))  # position, size, index
    for index, (gap_size, file_size) in enumerate(zip(gap_sizes, file_sizes[1:]), 1):
        files.append((files[-1][0] + files[-1][1] + gap_size, file_size, index))
    moved_files = files.copy()
    for file in reversed(files):
        for i in range(len(moved_files) - 1):
            if moved_files[i][2] == file[2]:
                break  # found self
            elif (
                moved_files[i + 1][0] - (moved_files[i][0] + moved_files[i][1])
                >= file[1]
            ):
                moved_files.remove(file)
                new_file = ((moved_files[i][0] + moved_files[i][1]), file[1], file[2])
                moved_files.insert(i + 1, new_file)
                break
    return moved_files


def solve_2(blocks: list[int], gaps: list[int]) -> int:
    moved_blocks = move_files_2(blocks, gaps)
    count = 0
    for position, size, index in moved_blocks:
        count += size * (position + position + size - 1) // 2 * index
    return count


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
    if "2" in argv:
        print(solve_2(blocks, gaps))
    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

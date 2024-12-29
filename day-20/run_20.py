from heapq import heapify, heappush, heappop
import numpy as np
import sys
import timeit


# taken verbatim from day 16
def parse(lines: list[str]) -> tuple[np.ndarray, tuple[int, int], tuple[int, int]]:
    start = (0, 0)
    end = (0, 0)
    maze = np.zeros((len(lines), len(lines[0]) - 1), dtype=bool)
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == "#":
                maze[i, j] = True
            elif c == "S":
                start = (i, j)
            elif c == "E":
                end = (i, j)
    return maze, start, end


# adapted from day 16
def walk(maze: np.ndarray, point: tuple[int, int]) -> np.ndarray:
    edges = []
    heapify(edges)
    heappush(edges, (0, point[0], point[1]))
    big_num = maze.size
    # practically infinite, larger than max possible distance

    path = big_num * np.ones_like(maze, dtype=int)

    while edges:
        score, i, j = heappop(edges)
        path[i, j] = score
        for di, dj in [(0, 1), (-1, 0), (0, -1), (1, 0)]:
            if not maze[i + di, j + dj] and (
                path[i + di, j + dj] == big_num or score < path[i + di, j + dj]
            ):
                heappush(edges, (score + 1, i + di, j + dj))
    return path


def find_cheats(
    dist_to_start: np.ndarray, dist_to_end: np.ndarray, honest_time: int
) -> np.ndarray:
    """
    Finds time savings at each passable wall
    """
    big_num = dist_to_start[0, 0]
    cheats = big_num * np.ones_like(dist_to_start, dtype=int)
    cheats[1:-1, :] = np.minimum(
        cheats[1:-1, :], dist_to_start[:-2, :] + dist_to_end[2:, :] + 2
    )
    cheats[1:-1, :] = np.minimum(
        cheats[1:-1, :], dist_to_start[2:, :] + dist_to_end[:-2, :] + 2
    )
    cheats[:, 1:-1] = np.minimum(
        cheats[:, 1:-1], dist_to_start[:, :-2] + dist_to_end[:, 2:] + 2
    )
    cheats[:, 1:-1] = np.minimum(
        cheats[:, 1:-1], dist_to_start[:, 2:] + dist_to_end[:, :-2] + 2
    )
    return cheats


def count_cheats(
    maze: np.ndarray, start: tuple[int, int], end: tuple[int, int]
) -> list[int]:
    """
    Lists time savings by passable wall
    """
    dist_to_start = walk(maze, start)
    honest_time = dist_to_start[end[0], end[1]]
    dist_to_end = walk(maze, end)
    cheats = find_cheats(dist_to_start, dist_to_end, honest_time)
    return (honest_time - cheats)[cheats < honest_time].tolist()


def render_cheats(
    cheats: np.ndarray, dist_to_start: np.ndarray, honest_time: int
) -> None:
    big_num = dist_to_start[0, 0]
    print(
        "\n".join(
            "".join(
                "*"
                if cheats[i, j] < honest_time
                else (
                    str(dist_to_start[i, j] % 10)
                    if dist_to_start[i, j] < big_num
                    else "#"
                )
                for j in range(dist_to_start.shape[1])
            )
            for i in range(dist_to_start.shape[0])
        )
    )


def solve_1(
    maze: np.ndarray, start: tuple[int, int], end: tuple[int, int], target: int
) -> int:
    return len([time for time in count_cheats(maze, start, end) if time >= target])


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv
    if argv[0] == "python":
        argv = argv[1:]
    with open(argv[-1]) as hin:
        input_lines = hin.readlines()
    maze, maze_start, end = parse(input_lines)
    start = timeit.default_timer()
    if "1" in argv:
        print(solve_1(maze, maze_start, end, 100))  # we have a target of 100 ps

    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

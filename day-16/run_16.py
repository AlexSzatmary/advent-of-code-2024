from heapq import heapify, heappush, heappop
import numpy as np
import sys
import timeit


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


def walk(
    maze: np.ndarray, start: tuple[int, int], end: tuple[int, int]
) -> tuple[int, np.ndarray]:
    edges = []
    heapify(edges)
    heappush(edges, (0, start[0], start[1], 0))
    # path is a 3D matrix with the third dimension having the reindeer pointed east or
    # west (0) versus north or south (1)
    rotate_cost = 1000
    big_num = (rotate_cost + 1) * maze.size
    # practically infinite, larger than max possible score

    path = big_num * np.ones((maze.shape[0], maze.shape[1], 2), dtype=int)
    min_score = big_num

    while edges:
        score, i, j, k = heappop(edges)
        path[i, j, k] = score
        if score > min_score:
            break
        if (i, j) == end:
            min_score = min(score, min_score)
        if k == 0:  # check east and west
            for dj in [-1, 1]:
                if not maze[i, j + dj] and (
                    path[i, j + dj, k] == 0 or score < path[i, j + dj, k]
                ):
                    heappush(edges, (score + 1, i, j + dj, k))
        else:  # check north and south
            for di in [-1, 1]:
                if not maze[i + di, j] and (
                    path[i + di, j, k] == 0 or score < path[i + di, j, k]
                ):
                    heappush(edges, (score + 1, i + di, j, k))
        if path[i, j, 1 - k] == 0 or score + rotate_cost < path[i, j, 1 - k]:
            # check rotating. It's kind of goofy to check turning in the middle of a
            # straight corridor but this makes the checks much simpler and I don't need
            # to track whether the reindeer is moving east versus west or north versus
            # south. This would be a problem if the reindeer started pointing east but
            # able to move west.
            heappush(edges, (score + rotate_cost, i, j, 1 - k))
    return min_score, path


def solve_1(maze: np.ndarray, start: tuple[int, int], end: tuple[int, int]) -> int:
    return walk(maze, start, end)[0]


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
        print(solve_1(maze, maze_start, end))

    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

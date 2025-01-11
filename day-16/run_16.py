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


def render_backtrack(maze: np.ndarray, path: np.ndarray, visited: np.ndarray) -> str:
    big_num = path[0, 0, 0]
    rows = []
    for i in range(maze.shape[0]):
        row = []
        for j in range(maze.shape[1]):
            if visited[i, j]:
                c = "O"
            elif path[i, j, 0] < big_num or path[i, j, 1] < big_num:
                c = str(min(path[i, j, 0], path[i, j, 1]) % 10)
            elif maze[i, j]:
                c = "#"
            else:
                c = "."
            row.append(c)
        rows.append("".join(row))
    return "\n".join(rows)


def walk(  # noqa: C901  No good way to make simpler
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
        if score > path[i, j, k]:
            continue
        path[i, j, k] = score
        if score > min_score:
            break
        if (i, j) == end:
            min_score = min(score, min_score)
        elif k == 0:  # check east and west
            for dj in [-1, 1]:
                if not maze[i, j + dj] and score < path[i, j + dj, k]:
                    heappush(edges, (score + 1, i, j + dj, k))
        else:  # check north and south
            for di in [-1, 1]:
                if not maze[i + di, j] and score < path[i + di, j, k]:
                    heappush(edges, (score + 1, i + di, j, k))
        if score + rotate_cost < path[i, j, 1 - k]:
            # check rotating. It's kind of goofy to check turning in the middle of a
            # straight corridor but this makes the checks much simpler and I don't need
            # to track whether the reindeer is moving east versus west or north versus
            # south. This would be a problem if the reindeer started pointing east but
            # able to move west.
            heappush(edges, (score + rotate_cost, i, j, 1 - k))
    return min_score, path


def solve_1(maze: np.ndarray, start: tuple[int, int], end: tuple[int, int]) -> int:
    return walk(maze, start, end)[0]


def backtrack(path: np.ndarray, end: tuple[int, int]) -> np.ndarray:
    visited = np.zeros((path.shape[0], path.shape[1]), dtype=bool)
    visited[end] = True
    rotate_cost = 1000
    edges = [(end[0], end[1], 1, path[end[0], end[1], 1])]
    new_edges = []
    while edges:
        for i, j, k, score in edges:
            if k == 0:  # check east and west
                for dj in [-1, 1]:
                    if path[i, j + dj, k] == score - 1:
                        new_edges.append((i, j + dj, k, score - 1))
                        visited[i, j + dj] = True
            else:  # check north and south
                for di in [-1, 1]:
                    if path[i + di, j, k] == score - 1:
                        new_edges.append((i + di, j, k, score - 1))
                        visited[i + di, j] = True
            if path[i, j, 1 - k] == score - rotate_cost:
                new_edges.append((i, j, 1 - k, score - rotate_cost))
                # no need to mark visited for rotate
        edges = new_edges
        new_edges = []
    return visited


def solve_2(maze: np.ndarray, start: tuple[int, int], end: tuple[int, int]) -> int:
    path = walk(maze, start, end)[1]
    visited = backtrack(path, end)
    assert visited[start]
    return np.sum(visited)


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
    if "2" in argv:
        print(solve_2(maze, maze_start, end))

    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

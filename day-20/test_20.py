import numpy as np
import os
import pytest
from run_20 import (
    parse,
    walk,
    render_cheats,
    find_cheats,
    solve_1,
    solve_2,
)


def load(file_name: str) -> list[str]:
    inex_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(inex_path) as hin:
        lines = hin.readlines()
    return lines


@pytest.fixture
def maze_1() -> tuple[np.ndarray, tuple[int, int], tuple[int, int]]:
    return parse(load("inex-20-1.txt"))


def test_parse(
    maze_1: tuple[np.ndarray, tuple[int, int], tuple[int, int]],
) -> None:
    maze, start, end = maze_1
    assert start == (3, 1)
    assert end == (7, 5)
    assert maze.shape == (15, 15)
    assert np.sum(maze) == 140


def test_walk(
    maze_1: tuple[np.ndarray, tuple[int, int], tuple[int, int]],
) -> None:
    maze, start, end = maze_1
    dist_to_start = walk(maze, start)
    honest_time = dist_to_start[end[0], end[1]]
    dist_to_end = walk(maze, end)
    assert honest_time == 84
    assert dist_to_end[start[0], start[1]] == 84
    big_num = dist_to_start[0, 0]
    assert np.sum(dist_to_start == big_num) == 140
    assert np.sum(dist_to_end == big_num) == 140


def test_solve_1(
    maze_1: tuple[np.ndarray, tuple[int, int], tuple[int, int]],
) -> None:
    maze, start, end = maze_1
    cheats_times = [
        (14, 2),
        (14, 4),
        (2, 6),
        (4, 8),
        (2, 10),
        (3, 12),
        (1, 20),
        (1, 36),
        (1, 38),
        (1, 40),
        (1, 64),
    ]
    cumulative_cheats = 0
    for n_cheats, target in reversed(cheats_times):
        cumulative_cheats += n_cheats
        assert solve_1(maze, start, end, target) == cumulative_cheats


def test_solve_2(
    maze_1: tuple[np.ndarray, tuple[int, int], tuple[int, int]],
) -> None:
    maze, start, end = maze_1
    cheats_times = [
        (32, 50),
        (31, 52),
        (29, 54),
        (39, 56),
        (25, 58),
        (23, 60),
        (20, 62),
        (19, 64),
        (12, 66),
        (14, 68),
        (12, 70),
        (22, 72),
        (4, 74),
        (3, 76),
    ]
    cumulative_cheats = 0
    for n_cheats, target in reversed(cheats_times):
        cumulative_cheats += n_cheats
        assert solve_2(maze, start, end, target) == cumulative_cheats


def test_render_cheats(
    maze_1: tuple[np.ndarray, tuple[int, int], tuple[int, int]],
) -> None:
    maze, start, end = maze_1
    dist_to_start = walk(maze, start)
    honest_time = dist_to_start[end[0], end[1]]
    dist_to_end = walk(maze, end)
    cheats = find_cheats(dist_to_start, dist_to_end, honest_time)
    render_cheats(cheats, dist_to_start, honest_time)

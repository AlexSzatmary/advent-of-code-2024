import numpy as np
import os
import pytest
from run_16 import (
    parse,
    solve_1,
    solve_2,
    walk,
    backtrack,
    render_backtrack,
)


def load(file_name: str) -> list[str]:
    inex_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(inex_path) as hin:
        lines = hin.readlines()
    return lines


@pytest.fixture
def maze_1() -> tuple[np.ndarray, tuple[int, int], tuple[int, int]]:
    return parse(load("inex-16-1.txt"))


@pytest.fixture
def maze_2() -> tuple[np.ndarray, tuple[int, int], tuple[int, int]]:
    return parse(load("inex-16-2.txt"))


def test_parse(
    maze_1: tuple[np.ndarray, tuple[int, int], tuple[int, int]],
) -> None:
    maze, start, end = maze_1
    assert start == (13, 1)
    assert end == (1, 13)
    assert maze.shape == (15, 15)
    assert np.sum(maze) == 121


# def test_render(
#     maze_1: tuple[np.ndarray, tuple[int, int], tuple[int, int]],
# ) -> None:


def test_solve_1(
    maze_1: tuple[np.ndarray, tuple[int, int], tuple[int, int]],
    maze_2: tuple[np.ndarray, tuple[int, int], tuple[int, int]],
) -> None:
    maze, start, end = maze_1
    assert solve_1(maze, start, end) == 7036
    maze, start, end = maze_2
    assert solve_1(maze, start, end) == 11048


def test_solve_2(
    maze_1: tuple[np.ndarray, tuple[int, int], tuple[int, int]],
    maze_2: tuple[np.ndarray, tuple[int, int], tuple[int, int]],
) -> None:
    maze, start, end = maze_1
    assert solve_2(maze, start, end) == 45
    maze, start, end = maze_2
    assert solve_2(maze, start, end) == 64


def test_render_backtrack(
    maze_1: tuple[np.ndarray, tuple[int, int], tuple[int, int]],
    maze_2: tuple[np.ndarray, tuple[int, int], tuple[int, int]],
) -> None:
    """
    Makes sure render function runs; does not check for correctness.
    """
    maze, start, end = maze_1
    path = walk(maze, start, end)[1]
    visited = backtrack(path, end)
    assert render_backtrack(maze, path, visited)
    maze, start, end = maze_2
    path = walk(maze, start, end)[1]
    visited = backtrack(path, end)
    assert render_backtrack(maze, path, visited)

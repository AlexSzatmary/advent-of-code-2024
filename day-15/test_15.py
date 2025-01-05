import numpy as np
import os
import pytest
from run_15 import (
    parse,
    move,
    # gps, not yet tested explicitly; it's easier to just test solve and move
    render,
    solve_1,
    convert_1_to_2,
    render_2,
    move_2,
    solve_2,
)
from inspect import cleandoc


def load(file_name: str) -> list[str]:
    inex_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(inex_path) as hin:
        lines = hin.readlines()
    return lines


@pytest.fixture
def crates_movements_1() -> tuple[int, int, np.ndarray, np.ndarray, str]:
    return parse(load("inex-15-1.txt"))


@pytest.fixture
def crates_movements_2() -> tuple[int, int, np.ndarray, np.ndarray, str]:
    return parse(load("inex-15-2.txt"))


@pytest.fixture
def crates_movements_3() -> tuple[int, int, np.ndarray, np.ndarray, str]:
    return parse(load("inex-15-3.txt"))


def test_parse(
    crates_movements_1: tuple[int, int, np.ndarray, np.ndarray, str],
) -> None:
    i, j, crates, walls, movements = crates_movements_1
    assert i == 4
    assert j == 4
    print(render(i, j, crates, walls))
    assert crates.shape == (10, 10)
    assert walls.shape == (10, 10)
    assert np.sum(crates) == 21
    assert np.sum(walls[1:-1, 1:-1]) == 1
    assert len(movements) > 200  # I eyeballed it and it looked like a lot


def test_render(
    crates_movements_1: tuple[int, int, np.ndarray, np.ndarray, str],
) -> None:
    i, j, crates, walls, _ = crates_movements_1
    reference = cleandoc("""
    ##########
    #..O..O.O#
    #......O.#
    #.OO..O.O#
    #..O@..O.#
    #O#..O...#
    #O..O..O.#
    #.OO.O.OO#
    #....O...#
    ##########
    """)
    s = render(i, j, crates, walls)
    assert s == reference


def test_move(
    crates_movements_1: tuple[int, int, np.ndarray, np.ndarray, str],
    crates_movements_2: tuple[int, int, np.ndarray, np.ndarray, str],
) -> None:
    i, j, crates, walls, movements = crates_movements_2
    print(render(i, j, crates, walls))
    i, j, crates = move(i, j, crates.copy(), walls, movements)
    print(render(i, j, crates, walls))
    assert (
        render(i, j, crates, walls)
        == cleandoc("""
        ########
        #....OO#
        ##.....#
        #.....O#
        #.#O@..#
        #...O..#
        #...O..#
        ########
        """)
    )

    i, j, crates, walls, movements = crates_movements_1
    i, j, crates = move(i, j, crates.copy(), walls, movements)
    assert render(i, j, crates, walls) == cleandoc(
        """
        ##########
        #.O.O.OOO#
        #........#
        #OO......#
        #OO@.....#
        #O#.....O#
        #O.....OO#
        #O.....OO#
        #OO....OO#
        ##########
        """
    )


def test_solve_1(
    crates_movements_1: tuple[int, int, np.ndarray, np.ndarray, str],
    crates_movements_2: tuple[int, int, np.ndarray, np.ndarray, str],
) -> None:
    i, j, crates, walls, movements = crates_movements_1
    assert solve_1(i, j, crates, walls, movements) == 10092
    i, j, crates, walls, movements = crates_movements_2
    assert solve_1(i, j, crates, walls, movements) == 2028


def test_convert_1_to_2(
    crates_movements_1: tuple[int, int, np.ndarray, np.ndarray, str],
) -> None:
    i, j, crates, walls, movements = crates_movements_1
    i, j, crates, walls, movements = convert_1_to_2(i, j, crates, walls, movements)
    assert i == 4
    assert j == 8
    assert crates.shape == (10, 20)
    assert walls.shape == (10, 20)
    assert np.sum(crates) == 21
    assert np.sum(walls[2:-2, 2:-2]) == 2
    assert len(movements) > 200  # I eyeballed it and it looked like a lot


def test_render_2(
    crates_movements_1: tuple[int, int, np.ndarray, np.ndarray, str],
) -> None:
    i, j, crates, walls, movements = crates_movements_1
    i, j, crates, walls, _ = convert_1_to_2(i, j, crates, walls, movements)
    reference = cleandoc("""
        ####################
        ##....[]....[]..[]##
        ##............[]..##
        ##..[][]....[]..[]##
        ##....[]@.....[]..##
        ##[]##....[]......##
        ##[]....[]....[]..##
        ##..[][]..[]..[][]##
        ##........[]......##
        ####################
        """)
    s = render_2(i, j, crates, walls)
    print(reference)
    print()
    print(s)
    assert s == reference


def test_move_2(
    crates_movements_1: tuple[int, int, np.ndarray, np.ndarray, str],
    crates_movements_3: tuple[int, int, np.ndarray, np.ndarray, str],
) -> None:
    i, j, crates, walls, movements = crates_movements_3
    i, j, crates, walls, movements = convert_1_to_2(i, j, crates, walls, movements)
    print(render_2(i, j, crates, walls))
    i, j, crates = move_2(i, j, crates.copy(), walls, movements)
    print(render_2(i, j, crates, walls))
    assert (
        render_2(i, j, crates, walls)
        == cleandoc("""
            ##############
            ##...[].##..##
            ##...@.[]...##
            ##....[]....##
            ##..........##
            ##..........##
            ##############
            """)
    )

    i, j, crates, walls, movements = crates_movements_1
    i, j, crates, walls, movements = convert_1_to_2(i, j, crates, walls, movements)
    i, j, crates = move_2(i, j, crates.copy(), walls, movements)
    assert render_2(i, j, crates, walls) == cleandoc(
        """
        ####################
        ##[].......[].[][]##
        ##[]...........[].##
        ##[]........[][][]##
        ##[]......[]....[]##
        ##..##......[]....##
        ##..[]............##
        ##..@......[].[][]##
        ##......[][]..[]..##
        ####################
        """
    )


def test_solve_2(
    crates_movements_1: tuple[int, int, np.ndarray, np.ndarray, str],
) -> None:
    i, j, crates, walls, movements = crates_movements_1
    i, j, crates, walls, movements = convert_1_to_2(i, j, crates, walls, movements)
    assert solve_2(i, j, crates, walls, movements) == 9021

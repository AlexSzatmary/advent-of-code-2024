import numpy as np
import sys
import timeit
from typing import cast, Literal, Union


def parse(lines: list[str]) -> tuple[int, int, np.ndarray, np.ndarray, str]:
    i_robot = 0
    j_robot = 0
    blank_index = lines.index("\n")
    crates = np.zeros((blank_index, len(lines[0]) - 1), dtype=bool)
    walls = np.zeros((blank_index, len(lines[0]) - 1), dtype=bool)
    for i, line in enumerate(lines[0:blank_index]):
        for j, c in enumerate(line):
            if c == "O":
                crates[i, j] = True
            elif c == "#":
                walls[i, j] = True
            elif c == "@":
                i_robot = i
                j_robot = j
    movements = "".join(s[:-1] for s in lines[blank_index + 1 :])
    return i_robot, j_robot, crates, walls, movements


def render(i_robot: int, j_robot: int, crates: np.ndarray, walls: np.ndarray) -> str:
    robot = np.zeros_like(crates)
    robot[i_robot, j_robot] = True
    return "\n".join(
        "".join(
            "O" if crates[i, j] else "#" if walls[i, j] else "@" if robot[i, j] else "."
            for j in range(crates.shape[1])
        )
        for i in range(crates.shape[0])
    )


def move(
    i_robot: int, j_robot: int, crates: np.ndarray, walls: np.ndarray, movements: str
) -> tuple[int, int, np.ndarray]:
    crates = crates.copy()
    for m in movements:
        m = cast(Union[Literal[">"], Literal["^"], Literal["<"], Literal["v"]], m)
        match m:
            case ">":
                di, dj = (0, 1)
            case "^":
                di, dj = (-1, 0)
            case "<":
                di, dj = (0, -1)
            case "v":
                di, dj = (1, 0)

        if crates[i_robot + di, j_robot + dj]:
            # this is the complicated branch
            # the closest empty space would be 2 away
            i_robot, j_robot, crates = maybe_move_crate(
                i_robot, j_robot, di, dj, crates, walls
            )
        elif not walls[i_robot + di, j_robot + dj]:
            i_robot += di
            j_robot += dj
        else:  # walls[i_robot + di, j_robot + dj]:
            pass  # the robot hits a wall directly and does not move
        # print(f"Move: {m}")
        # print(render(i_robot, j_robot, crates, walls))
        # print()
    return i_robot, j_robot, crates


def maybe_move_crate(
    i_robot: int, j_robot: int, di: int, dj: int, crates: np.ndarray, walls: np.ndarray
) -> tuple[int, int, np.ndarray]:
    i_to = i_robot + di * 2
    j_to = j_robot + dj * 2
    while True:
        if crates[i_to, j_to]:
            i_to += di
            j_to += dj
        elif not walls[i_to, j_to]:
            # move the crate
            crates[i_robot + di, j_robot + dj] = False
            crates[i_to, j_to] = True
            # move the robot
            i_robot += di
            j_robot += dj
            break
        else:  # wall
            break
    return i_robot, j_robot, crates


def gps(crates: np.ndarray) -> int:
    total_coordinates = sum(
        100 * i + j
        for i, row in enumerate(crates)
        for j, tile in enumerate(row)
        if crates[i, j]
    )
    return total_coordinates


def solve_1(
    i: int, j: int, crates: np.ndarray, walls: np.ndarray, movements: str
) -> int:
    i, j, crates = move(i, j, crates.copy(), walls, movements)
    return gps(crates)


def convert_1_to_2(
    i_robot: int, j_robot: int, crates: np.ndarray, walls: np.ndarray, movements: str
) -> tuple[int, int, np.ndarray, np.ndarray, str]:
    # the east-west direction is doubled
    # double j
    # stretch crates and use True to indicate that the left side of a crate is on a tile
    # (and the right side is on the tile to its right, which would be False)
    # we simply double up the walls
    j_robot *= 2
    crates_2 = np.zeros((crates.shape[0], 2 * crates.shape[1]), dtype=bool)
    crates_2[:, ::2] = crates
    walls_2 = np.zeros((walls.shape[0], 2 * walls.shape[1]), dtype=bool)
    walls_2[:, 0::2] = walls
    walls_2[:, 1::2] = walls
    return i_robot, j_robot, crates_2, walls_2, movements


def render_2(i_robot: int, j_robot: int, crates: np.ndarray, walls: np.ndarray) -> str:
    robot = np.zeros_like(crates)
    robot[i_robot, j_robot] = True
    return "\n".join(
        "".join(
            "["
            if crates[i, j]
            else "]"
            if crates[i, j - 1]
            else "#"
            if walls[i, j]
            else "@"
            if robot[i, j]
            else "."
            for j in range(crates.shape[1])
        )
        for i in range(crates.shape[0])
    )


def move_2(
    i_robot: int, j_robot: int, crates: np.ndarray, walls: np.ndarray, movements: str
) -> tuple[int, int, np.ndarray]:
    crates = crates.copy()
    for m in movements:
        m = cast(Union[Literal[">"], Literal["^"], Literal["<"], Literal["v"]], m)
        match m:
            case ">":
                di, dj = (0, 1)
            case "^":
                di, dj = (-1, 0)
            case "<":
                di, dj = (0, -1)
            case "v":
                di, dj = (1, 0)

        if crates[i_robot + di, j_robot + dj] or crates[i_robot + di, j_robot + dj - 1]:
            # this is the complicated branch
            if m == ">":
                i_robot, j_robot, crates = maybe_move_crate_2_e(
                    i_robot, j_robot, crates, walls
                )
            elif m == "<":
                i_robot, j_robot, crates = maybe_move_crate_2_w(
                    i_robot, j_robot, crates, walls
                )
            else:
                i_robot, j_robot, crates = maybe_move_crate_2_ns(
                    i_robot, j_robot, di, crates, walls
                )
        elif not walls[i_robot + di, j_robot + dj]:
            i_robot += di
            j_robot += dj
        else:  # walls[i_robot + di, j_robot + dj]:
            pass  # the robot hits a wall directly and does not move
        # print(f"Move: {m}")
        # print(render_2(i_robot, j_robot, crates, walls))
        # print()
        # input()
    return i_robot, j_robot, crates


def maybe_move_crate_2_e(
    i_robot: int, j_robot: int, crates: np.ndarray, walls: np.ndarray
) -> tuple[int, int, np.ndarray]:
    # @[][].#
    # ^^.^..#
    # 012345#
    j_to = j_robot + 3
    while True:
        if crates[i_robot, j_to]:
            j_to += 2
        elif not walls[i_robot, j_to]:
            # move the crate
            crates[i_robot, j_robot + 2 : j_to + 1] = crates[
                i_robot, j_robot + 1 : j_to
            ]
            crates[i_robot, j_robot + 1] = False
            # move the robot
            j_robot += 1
            break
        else:  # wall
            break
    return i_robot, j_robot, crates


def maybe_move_crate_2_w(
    i_robot: int, j_robot: int, crates: np.ndarray, walls: np.ndarray
) -> tuple[int, int, np.ndarray]:
    # #.[][]@
    # #543210
    j_to = j_robot - 4
    while True:
        if crates[i_robot, j_to]:
            j_to -= 2
        elif not walls[i_robot, j_to + 1]:
            # move the crate
            crates[i_robot, j_to : j_robot - 1] = crates[i_robot, j_to + 1 : j_robot]
            crates[i_robot, j_robot - 1] = False
            # move the robot
            j_robot -= 1
            break
        else:  # wall
            break
    return i_robot, j_robot, crates


def maybe_move_crate_2_ns(
    i_robot: int, j_robot: int, di: int, crates: np.ndarray, walls: np.ndarray
) -> tuple[int, int, np.ndarray]:
    # throughout, I presume we're trying to move up (di = -1) but everything reverses
    # fine to go down.

    # I'm managing wide crates by marking their left coordinate. Therefore, a crate can
    # be:
    # * above or above and to the left of the robot
    # * above, above and to the left, or above and to the right of a crate. A crate can
    # be below 0, 1, or 2 crates
    # * below a wall, or below and to the right of a wall
    all_crates = [
        (i_robot + di, j) for j in [j_robot - 1, j_robot] if crates[i_robot + di, j]
    ]  # this should select just one crate
    crates_to_check = all_crates.copy()
    crates_to_check_next = []

    can_move = False

    while True:
        any_walls = [
            (i + di, j)
            for i, j_crate in crates_to_check
            for j in [j_crate, j_crate + 1]
            if walls[i + di, j]
        ]
        crates_to_check_next = {
            (i + di, j)
            for i, j_crate in crates_to_check
            for j in [j_crate - 1, j_crate, j_crate + 1]
            if crates[i + di, j]
        }
        crates_to_check = crates_to_check_next
        all_crates.extend(crates_to_check)
        if not crates_to_check_next and not any_walls:
            can_move = True
            break
        elif any_walls:  # wall
            break

    if can_move:
        # we need reversed so we move the top crates up first
        for crate_i, crate_j in reversed(all_crates):
            # move the crates
            crates[crate_i, crate_j] = False
            crates[crate_i + di, crate_j] = True
        # move the robot
        i_robot += di

    return i_robot, j_robot, crates


def solve_2(
    i: int, j: int, crates: np.ndarray, walls: np.ndarray, movements: str
) -> int:
    i, j, crates = move_2(i, j, crates.copy(), walls, movements)
    return gps(crates)


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv
    if argv[0] == "python":
        argv = argv[1:]
    with open(argv[-1]) as hin:
        input_lines = hin.readlines()
    i, j, crates, walls, movements = parse(input_lines)
    start = timeit.default_timer()
    if "1" in argv:
        print(solve_1(i, j, crates, walls, movements))
    if "2" in argv:
        i, j, crates, walls, movements = convert_1_to_2(i, j, crates, walls, movements)
        print(solve_2(i, j, crates, walls, movements))

    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

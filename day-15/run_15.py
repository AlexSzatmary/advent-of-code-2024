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

    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

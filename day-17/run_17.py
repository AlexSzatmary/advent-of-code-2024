import re
import sys
import timeit


def parse(lines: list[str]) -> tuple[int, int, int, list[int]]:
    reg_A = 0
    reg_B = 0
    reg_C = 0
    program = []
    for line in lines:
        if m := re.match(r"Register A: (\d+)", line):
            reg_A = int(m.group(1))
        if m := re.match(r"Register B: (\d+)", line):
            reg_B = int(m.group(1))
        if m := re.match(r"Register C: (\d+)", line):
            reg_C = int(m.group(1))
        if m := re.match(r"Program: ((\d|,)+)", line):
            program = list(map(int, m.group(1).split(",")))
    return reg_A, reg_B, reg_C, program


def interpret(  # noqa: C901 The complexity of this function is unavoidable
    reg_A: int,
    reg_B: int,
    reg_C: int,
    program: list[int],
) -> list[int]:
    output = []
    ip = 0  # instruction pointer

    def combo(operand: int) -> int:
        if operand < 4:
            return operand
        elif operand == 4:
            return reg_A
        elif operand == 5:
            return reg_B
        elif operand == 6:
            return reg_C
        else:
            e = f"operand {operand} not valid"
            raise ValueError(e)

    while ip < len(program):
        operand = program[ip + 1]
        match program[ip]:
            case 0:  # adv division
                reg_A >>= combo(operand)
            case 1:  # bxl
                reg_B = reg_B ^ operand
            case 2:  # bst
                reg_B = combo(operand) % 8
            case 3:  # jnz
                if reg_A:
                    ip = operand - 2  # ip will be increased by 2 later
            case 4:  # bxc
                reg_B ^= reg_C
            case 5:  # out
                output.append(combo(operand) % 8)
            case 6:  # bdv
                reg_B = reg_A >> combo(operand)
            case 7:  # cdv
                reg_C = reg_A >> combo(operand)
        ip += 2

    return output


def solve_1(reg_A: int, reg_B: int, reg_C: int, program: list[int]) -> str:
    return ",".join(map(str, interpret(reg_A, reg_B, reg_C, program)))


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv
    if argv[0] == "python":
        argv = argv[1:]
    with open(argv[-1]) as hin:
        input_lines = hin.readlines()
    reg_A, reg_B, reg_C, program = parse(input_lines)
    start = timeit.default_timer()
    if "1" in argv:
        print(solve_1(reg_A, reg_B, reg_C, program))

    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

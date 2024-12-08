from collections import defaultdict
import pathlib
import sys
import timeit


def parse(L: list[str]) -> tuple[list[tuple[int, int]], list[list[int]]]:
    rules = []
    updates = []
    for s in L:
        if "|" in s:
            rules.append(tuple(map(int, s.split("|"))))
        elif "," in s:
            updates.append(list(map(int, s.split(","))))
    return rules, updates


def check_update(rules: list[tuple[int, int]], update: list[int]) -> bool:
    for before, after in rules:
        if update.index(before) > update.index(after):
            return False
    return True


def get_relevant_rules(
    rules: list[tuple[int, int]], update: list[int]
) -> list[tuple[int, int]]:
    # I need to get only the relevant rules, because all of the rules form a cyclic
    # graph; it so happens that the relevant rules for an update only form DAGs.
    return [rule for rule in rules if rule[0] in update and rule[1] in update]


def sort_rules(rules: list[tuple[int, int]]) -> list[int]:
    L_sorted = []
    s_sorted = set()
    s_all_nodes = set()
    d_before = defaultdict(set)
    for before, after in rules:
        d_before[after].add(before)
        s_all_nodes.add(after)
        s_all_nodes.add(before)
    left_node = next(node for node in s_all_nodes if node not in d_before)
    L_sorted.append(left_node)
    s_sorted.add(left_node)
    while d_before:
        for node, before in d_before.items():
            if before <= s_sorted:
                L_sorted.append(node)
                s_sorted.add(node)
                del d_before[node]
                break
    return L_sorted


def solve(rules: list[tuple[int, int]], updates: list[list[int]]) -> int:
    total_middle_numbers = 0
    for update in updates:
        relevant_rules = get_relevant_rules(rules, update)
        if not check_update(relevant_rules, update):
            update_sorted = sort_rules(relevant_rules)
            total_middle_numbers += update_sorted[(len(update) - 1) // 2]
    return total_middle_numbers


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv
    if argv[0] == "python":
        argv = argv[1:]
    with open(argv[1]) as hin:
        L = hin.readlines()
    rules, updates = parse(L)
    if "graphviz" in argv:
        with open(pathlib.Path(argv[1]).stem + ".dot", "w") as hout:
            hout.write("digraph {\n")
            for before, after in rules:
                hout.write(f"{before} -> {after}\n")
            hout.write("}\n")
        # invoke graphviz with, e.g.,
        # dot -Tpng < inme-05.dot>inme-05.png
    start = timeit.default_timer()
    print(solve(rules, updates))
    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

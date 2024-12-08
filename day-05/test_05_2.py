import run_05_2
import os

inex_path = os.path.join(os.path.dirname(__file__), "inex-05-1.txt")
with open(inex_path) as hin:
    inex_1 = hin.readlines()


def test_parse():
    rules, updates = run_05_2.parse(inex_1)
    assert len(rules)
    assert rules[-1] == (53, 13)
    assert len(updates) == 6
    assert updates[-1] == [97, 13, 75, 29, 47]


def test_sort_rules():
    # For this example, the rules are coherent so if you sort them, you get a
    # passable mock update
    rules, _ = run_05_2.parse(inex_1)
    sort_rules = run_05_2.sort_rules(rules)
    assert len(sort_rules)
    assert run_05_2.check_update(rules, sort_rules)


def test_partial_solve():
    rules, updates = run_05_2.parse(inex_1)
    references = [[97, 75, 47, 61, 53], [61, 29, 13], [97, 75, 47, 29, 13]]
    for i, update in enumerate(updates[3:]):
        relevant_rules = run_05_2.get_relevant_rules(rules, update)
        assert run_05_2.sort_rules(relevant_rules) == references[i]


def test_solve():
    rules, updates = run_05_2.parse(inex_1)
    assert run_05_2.solve(rules, updates) == 123

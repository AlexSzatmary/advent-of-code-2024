import run_05_1
import os

inex_path = os.path.join(os.path.dirname(__file__), "inex-05-1.txt")
with open(inex_path) as hin:
    inex_1 = hin.readlines()


def test_parse():
    rules, updates = run_05_1.parse(inex_1)
    assert len(rules)
    assert rules[-1] == (53, 13)
    assert len(updates) == 6
    assert updates[-1] == [97, 13, 75, 29, 47]


def test_check_update():
    rules, updates = run_05_1.parse(inex_1)
    reference = [True, True, True, False, False, False]
    assert [run_05_1.check_update(rules, update) for update in updates] == reference


def test_solve():
    rules, updates = run_05_1.parse(inex_1)
    assert run_05_1.solve(rules, updates) == 143

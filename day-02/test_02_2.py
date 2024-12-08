import run_02_2
import os

inex_path = os.path.join(os.path.dirname(__file__), "inex-02-1.txt")
with open(inex_path) as hin:
    inex_1 = hin.readlines()


def test_parse():
    reports = run_02_2.parse(inex_1)
    assert len(reports) == 6
    assert all(len(report) == 5 for report in reports)
    assert all(type(level) is int for report in reports for level in report)


def test_is_safe_with_dampener():
    reports = run_02_2.parse(inex_1)
    references = [True, False, False, True, True, True]
    assert all(
        run_02_2.is_safe_with_dampener(report) == reference
        for (report, reference) in zip(reports, references)
    )
    assert run_02_2.is_safe_with_dampener([1, 2, 3, 4, 10])


def test_solve():
    reports = run_02_2.parse(inex_1)
    assert run_02_2.solve(reports) == 4

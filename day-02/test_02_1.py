import run_02_1
import os

inex_path = os.path.join(os.path.dirname(__file__), "inex-02-1.txt")
with open(inex_path) as hin:
    inex_1 = hin.readlines()


def test_parse():
    reports = run_02_1.parse(inex_1)
    assert len(reports) == 6
    assert all(len(report) == 5 for report in reports)
    assert all(type(level) is int for report in reports for level in report)


def test_is_safe():
    reports = run_02_1.parse(inex_1)
    references = [True, False, False, False, False, True]
    assert all(
        run_02_1.is_safe(report) == reference
        for (report, reference) in zip(reports, references)
    )


def test_solve():
    reports = run_02_1.parse(inex_1)
    assert run_02_1.solve(reports) == 2

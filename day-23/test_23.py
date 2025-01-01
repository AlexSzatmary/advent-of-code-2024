from inspect import cleandoc
import os
import pytest
from run_23 import (
    parse,
    find_triples_including_t,
    solve_1,
)


def load(file_name: str) -> list[str]:
    inex_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(inex_path) as hin:
        lines = hin.readlines()
    return lines


@pytest.fixture
def network_1() -> dict[str, list[str]]:
    return parse(load("inex-23-1.txt"))


def test_parse(network_1: dict[str, list[str]]) -> None:
    network = network_1
    assert sum(len(children) for children in network.values()) == 32
    assert sorted(network["kh"]) == sorted(["tc", "qp", "ub", "ta"])


def test_find_triples_including_t(network_1: dict[str, list[str]]) -> None:
    network = network_1
    references = cleandoc("""
    co,de,ta
    co,ka,ta
    de,ka,ta
    qp,td,wh
    tb,vc,wq
    tc,td,wh
    td,wh,yn
    """).split("\n")
    # the reference is already ordered alphabetically and each triple is also ordered
    ref_triples = [tuple(line.split(",")) for line in references]
    triples = find_triples_including_t(network)
    print(triples)
    for triple, ref_triple in zip(sorted(triples), ref_triples):
        assert triple == ref_triple


def test_solve_1(network_1: dict[str, list[str]]) -> None:
    network = network_1
    assert solve_1(network) == 7

from collections import defaultdict
import sys
import timeit


def parse(lines: list[str]) -> defaultdict[str, list[str]]:
    """
    Given input file of pairs, creates network

    Parameters
    ----------
    lines : text of input file as list of strings

    Returns
    -------
    network : default dict giving list of connected nodes for a given node. The network
        is actually undirected but is represented here as a DAG for later purposes,
        with the "parent" in each pair being the one that is first alphabetically.
    """
    network = defaultdict(list)
    for line in lines:
        a = line[0:2]
        b = line[3:5]
        if b < a:
            a, b = b, a
        network[a].append(b)
    for node, children in network.items():
        network[node] = sorted(children)
    return network


def find_triples_including_t(
    network: dict[str, list[str]],
) -> list[tuple[str, str, str]]:
    triples = []
    for node_a, children in network.items():
        for i, node_b in enumerate(children[:-1]):
            for node_c in children[i + 1 :]:
                if (
                    node_b in network
                    and node_c in network[node_b]
                    and (
                        node_a.startswith("t")
                        or node_b.startswith("t")
                        or node_c.startswith("t")
                    )
                ):
                    triples.append((node_a, node_b, node_c))
    return triples


def solve_1(network: dict[str, list[str]]) -> int:
    return len(find_triples_including_t(network))


def find_largest_cluster(network: dict[str, list[str]]) -> tuple[str, int]:
    largest_cluster_so_far, largest_cluster_size = "", 0
    for node, children in network.items():
        largest_cluster_so_far, largest_cluster_size = find_largest_cluster_including(
            network,
            [node],
            children,
            largest_cluster_so_far,
            largest_cluster_size,
        )
    return largest_cluster_so_far, largest_cluster_size


def find_largest_cluster_including(
    network: dict[str, list[str]],
    cluster: list[str],
    possible_children: list[str],
    largest_cluster_so_far: str,
    largest_cluster_size: int,
) -> tuple[str, int]:
    if len(cluster) > largest_cluster_size:
        largest_cluster_so_far = ",".join(cluster)
        largest_cluster_size = len(cluster)
    for child in possible_children:
        if child in network:
            new_possible_children = [
                c for c in network[child] if c in possible_children
            ]
        else:
            new_possible_children = []
        if len(cluster) + 1 + len(new_possible_children) > largest_cluster_size:
            largest_cluster_so_far, largest_cluster_size = (
                find_largest_cluster_including(
                    network,
                    [*cluster, child],
                    new_possible_children,
                    largest_cluster_so_far,
                    largest_cluster_size,
                )
            )
    return largest_cluster_so_far, largest_cluster_size


def solve_2(network: dict[str, list[str]]) -> str:
    return find_largest_cluster(network)[0]


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv
    if argv[0] == "python":
        argv = argv[1:]
    with open(argv[-1]) as hin:
        input_lines = hin.readlines()
    network = parse(input_lines)
    start = timeit.default_timer()
    if "1" in argv:
        print(solve_1(network))
    if "2" in argv:
        print(solve_2(network))

    stop = timeit.default_timer()
    if "time" in argv:
        print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())

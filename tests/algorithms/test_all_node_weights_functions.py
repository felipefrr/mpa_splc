import networkx as nx
import pytest

from src.algorithms.dag import get_syncs
from src.algorithms.node_weights import calculate_n_all_minus, calculate_n_plus


class DigraphExamples:
    def __init__(self):
        self.edges = [['A', 'C'], ['C', 'E'], ['C', 'H'], ['E', 'G'], ['G', 'H'], ['H', 'K'],
                      ['B', 'C'], ['B', 'D'], ['B', 'J'], ['D', 'F'], ['D', 'I'], ['F', 'H'],
                      ['F', 'I'], ['I', 'L'], ['I', 'M'], ['J', 'M'], ['M', 'N']]
        self.G = nx.DiGraph()
        self.G.add_edges_from(self.edges)
        self.nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']
        self.syncs = get_syncs(self.G)
        self.topologic_order = list(nx.topological_sort(self.G))


@pytest.fixture()
def di_G():
    return DigraphExamples()


def test_calculate_n_minus_all_correctness(di_G):
    for node in di_G.topologic_order:
        calculate_n_all_minus(di_G.G, node)

    n_minus_all_expected = [1, 1, 3, 2, 2, 4, 3, 5, 6, 12, 7, 9, 13, 10]
    for index, node in enumerate(di_G.topologic_order):
        assert di_G.G.nodes[node]["Nall-"] == n_minus_all_expected[index]


def test_calculate_n_plus_correctness(di_G):
    reversed_top_order = list(reversed(di_G.topologic_order))
    for node in reversed_top_order:
        calculate_n_plus(di_G.G, node, di_G.syncs)

    n_plus_expected = [1, 1, 1, 1, 1, 2, 1, 3, 1, 1, 5, 2, 8, 2]
    for index, node in enumerate(reversed_top_order):
        assert di_G.G.nodes[node]["N+"] == n_plus_expected[index]

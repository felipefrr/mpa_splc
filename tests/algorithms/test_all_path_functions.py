import networkx as nx
import pytest

from src.algorithms.dag import get_syncs
from src.algorithms.edge_weights import calculate_splc_optimized
from src.algorithms.paths import main_path


class DigraphExamples:
    def __init__(self):
        self.edges = [['source', 'A'], ['source', 'B'],
                      ['A', 'C'], ['C', 'E'], ['C', 'H'], ['E', 'G'], ['G', 'H'], ['H', 'K'],
                      ['B', 'C'], ['B', 'D'], ['B', 'J'], ['D', 'F'], ['D', 'I'], ['F', 'H'],
                      ['F', 'I'], ['I', 'L'], ['I', 'M'], ['J', 'M'], ['M', 'N'],
                      ['K', 'sync'], ['L', 'sync'], ['N', 'sync']]
        self.G = nx.DiGraph()
        self.G.add_edges_from(self.edges)
        self.syncs = get_syncs(self.G)
        calculate_splc_optimized(self.G, self.syncs)


@pytest.fixture()
def di_G():
    return DigraphExamples()

@pytest.mark.filterwarnings("ignore::UserWarning")
def test_empty():
    G = nx.DiGraph()
    assert main_path(G) == []


def test_basic_main_path_longest(di_G):
    expected_main_path = ['source', 'B', 'D', 'F', 'I', 'M', 'N', 'sync']
    founded_main_path = main_path(di_G.G)
    assert expected_main_path == founded_main_path


@pytest.mark.skip(reason="Needs refactoring.")
def test_basic_main_path_shortest(di_G):
    expected_main_path = ['source', 'A', 'C', 'H', 'K', 'sync']
    founded_main_path = main_path(di_G.G, method='shortest')
    assert expected_main_path == founded_main_path


def test_not_supported_method(di_G):
    with pytest.raises(ValueError):
        main_path(di_G.G, method='bellman-ford')

import networkx as nx
import pytest

from src.algorithms.edge_weights import calculate_splc_optimized
from src.algorithms.dag import get_syncs
from src.algorithms.paths import main_path


class DigraphExamples:
    def __init__(self):
        self.edges = [['A', 'C'], ['C', 'E'], ['C', 'H'], ['E', 'G'], ['G', 'H'], ['H', 'K'],
                      ['B', 'C'], ['B', 'D'], ['B', 'J'], ['D', 'F'], ['D', 'I'], ['F', 'H'],
                      ['F', 'I'], ['I', 'L'], ['I', 'M'], ['J', 'M'], ['M', 'N']]
        self.G = nx.DiGraph()
        self.G.add_edges_from(self.edges)
        self.syncs = get_syncs(self.G)


@pytest.fixture()
def di_G():
    return DigraphExamples()


@pytest.mark.benchmark(group="Main Path")
def test_calc_splc_optimized(benchmark, di_G):
    calculate_splc_optimized(di_G.G, di_G.syncs)

    @benchmark
    def main_path_splc():
        main_path(di_G.G)


import networkx as nx
import pytest

from src.algorithms.edge_weights import calculate_spc, calculate_splc_fast, calculate_splc, calculate_splc_optimized
from src.algorithms.graphs import get_syncs, get_sources


class DigraphExamples:
    def __init__(self):
        self.edges = [['A', 'C'], ['C', 'E'], ['C', 'H'], ['E', 'G'], ['G', 'H'], ['H', 'K'],
                      ['B', 'C'], ['B', 'D'], ['B', 'J'], ['D', 'F'], ['D', 'I'], ['F', 'H'],
                      ['F', 'I'], ['I', 'L'], ['I', 'M'], ['J', 'M'], ['M', 'N']]
        self.G = nx.DiGraph()
        self.G.add_edges_from(self.edges)
        self.sources = get_sources(self.G)
        self.syncs = get_syncs(self.G)


@pytest.fixture()
def di_G():
    return DigraphExamples()


@pytest.mark.benchmark(group="SPC")
def test_calc_spc(benchmark, di_G):
    @benchmark
    def spc():
        calculate_spc(di_G.G, di_G.sources, di_G.syncs)


@pytest.mark.benchmark(group="SPLC")
def test_calc_splc(benchmark, di_G):
    @benchmark
    def splc():
        calculate_splc(di_G.G, di_G.syncs)

@pytest.mark.benchmark(group="SPLC")
def test_calc_splc_fast(benchmark, di_G):
    @benchmark
    def splc_fast():
        calculate_splc_fast(di_G.G, di_G.sources, di_G.syncs)

@pytest.mark.benchmark(group="SPLC")
def test_calc_splc_optimized(benchmark, di_G):
    @benchmark
    def splc_fast():
        calculate_splc_optimized(di_G.G, di_G.syncs)
import networkx as nx
import pytest

from src.algorithms.edge_weights import calculate_spc, calculate_splc_fast, calculate_splc
from src.algorithms.graphs import get_syncs, get_sources


def basic_digraph():
    edges = [['A', 'C'], ['C', 'E'], ['C', 'H'], ['E', 'G'], ['G', 'H'], ['H', 'K'],
             ['B', 'C'], ['B', 'D'], ['B', 'J'], ['D', 'F'], ['D', 'I'], ['F', 'H'],
             ['F', 'I'], ['I', 'L'], ['I', 'M'], ['J', 'M'], ['M', 'N']]
    G = nx.DiGraph()
    G.add_edges_from(edges)
    return G, edges


@pytest.mark.benchmark(group="SPC")
def test_calc_spc(benchmark):
    G, _ = basic_digraph()

    @benchmark
    def spc():
        calculate_spc(G, get_sources(G), get_syncs(G))


@pytest.mark.benchmark(group="SPLC")
def test_calc_splc(benchmark):
    G, _ = basic_digraph()

    @benchmark
    def splc():
        calculate_splc(G, get_syncs(G))


@pytest.mark.benchmark(group="SPLC")
def test_calc_splc_fast(benchmark):
    G, _ = basic_digraph()

    @benchmark
    def splc_fast():
        calculate_splc_fast(G, get_sources(G), get_syncs(G))

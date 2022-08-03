# import pytest
import networkx as nx

from src.algorithms.graphs import get_syncs, get_sources
from src.algorithms.edge_weights import calculate_spc, calculate_splc_fast, calculate_splc


def basic_digraph():
    edges = [['A', 'C'], ['C', 'E'], ['C', 'H'], ['E', 'G'], ['G', 'H'], ['H', 'K'],
             ['B', 'C'], ['B', 'D'], ['B', 'J'], ['D', 'F'], ['D', 'I'], ['F', 'H'],
             ['F', 'I'], ['I', 'L'], ['I', 'M'], ['J', 'M'], ['M', 'N']]
    G = nx.DiGraph()
    G.add_edges_from(edges)
    return G, edges


def test_calculate_spc_correctness():
    G, edges = basic_digraph()
    calculate_spc(G, get_sources(G), get_syncs(G))
    spc_expected = [2, 2, 2, 2, 2, 5, 2, 5, 1, 3, 2, 1, 2, 2, 2, 1, 3]
    for i in range(len(edges)):
        assert G[edges[i][0]][edges[i][1]]["SPC"] == spc_expected[i]


def test_calculate_splc_fast_correctness():
    G, edges = basic_digraph()
    calculate_splc_fast(G, get_sources(G), get_syncs(G))
    splc_expected = [2, 3, 3, 4, 5, 12, 2, 5, 1, 6, 4, 3, 6, 6, 6, 2, 9]
    for i in range(len(edges)):
        assert G[edges[i][0]][edges[i][1]]["SPLC"] == splc_expected[i]


def test_calculate_splc_correctness():
    G, edges = basic_digraph()
    calculate_splc(G, get_syncs(G))
    splc_expected = [2, 3, 3, 4, 5, 12, 2, 5, 1, 6, 4, 3, 6, 6, 6, 2, 9]
    for i in range(len(edges)):
        assert G[edges[i][0]][edges[i][1]]["SPLC"] == splc_expected[i]

# import pytest
import networkx as nx

from src.algorithms.graphs import get_syncs, get_sources, path_contain_edge


def test_dummy_graph():
    G = nx.DiGraph()
    assert not get_syncs(G)
    assert not get_syncs(G)


def test_one_source():
    G = nx.DiGraph([(0, 1), (1, 2)])
    assert get_sources(G) == [0]


def test_multiple_sources():
    G = nx.DiGraph([(0, 1), (1, 2), (3, 2), (4, 1), (2, 5)])
    assert get_sources(G) == [0, 3, 4]


def test_one_sync():
    G = nx.DiGraph([(0, 1), (1, 2)])
    assert get_syncs(G) == [2]


def test_multiple_syncs():
    G = nx.DiGraph([(0, 1), (1, 2), (3, 2), (3, 4), (2, 5)])
    assert get_syncs(G) == [4, 5]


def test_path_contain_edge():
    paths = ['A', 'D', 'J', 'K', 'H', 'B', 'F']
    edge = ['H', 'B']
    assert path_contain_edge(edge, paths)


def test_path_does_not_contain_edge():
    paths = ['A', 'D', 'J', 'K', 'H', 'B', 'F']
    edge = ['D', 'F']
    assert not path_contain_edge(edge, paths)

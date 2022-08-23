import networkx as nx

from src.algorithms.dag import get_syncs, get_sources, path_contain_edge, remove_cycles, add_artificial_source_sync


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


def test_remove_cycles_case1():
    G = nx.DiGraph()
    G.add_edge('A', 'B', pln_date=1)
    G.add_edge('C', 'D', pln_date=1)
    G.add_edge('B', 'E', pln_date=2)
    G.add_edge('D', 'F', pln_date=2)
    G.add_edge('B', 'D', pln_date=3)
    G.add_edge('D', 'B', pln_date=3)
    remove_cycles(G)
    assert nx.is_directed_acyclic_graph(G)
    assert (not G.has_edge('D', 'B') or not G.has_edge('B', 'D'))


def test_remove_cycles_case2():
    G = nx.DiGraph()
    G.add_edge('A', 'B', pln_date=1)
    G.add_edge('C', 'D', pln_date=1)
    G.add_edge('B', 'E', pln_date=3)
    G.add_edge('D', 'F', pln_date=4)
    G.add_edge('B', 'D', pln_date=1)
    G.add_edge('D', 'G', pln_date=2)
    G.add_edge('G', 'B', pln_date=1)
    G.add_edge('G', 'E', pln_date=3)
    remove_cycles(G)
    assert nx.is_directed_acyclic_graph(G)
    assert (not G.has_edge('G', 'B') or not G.has_edge('B', 'G'))


def test_remove_cycles_case3():
    G = nx.DiGraph()
    G.add_edge('A', 'C', pln_date=1)
    G.add_edge('C', 'D', pln_date=2)
    G.add_edge('D', 'E', pln_date=2)
    G.add_edge('E', 'F', pln_date=3)
    G.add_edge('E', 'C', pln_date=2)
    G.add_edge('B', 'G', pln_date=1)
    G.add_edge('G', 'H', pln_date=1)
    G.add_edge('H', 'G', pln_date=1)
    G.add_edge('H', 'F', pln_date=5)
    remove_cycles(G)
    edges = [('H', 'G'), ('E', 'C')]
    assert nx.is_directed_acyclic_graph(G)
    for edge in edges:
        u, v = edge
        assert (not G.has_edge(u, v) or not G.has_edge(v, u))


def test_add_artificial_source_sync_dummy():
    G = nx.DiGraph()
    add_artificial_source_sync(G)
    assert not get_sources(G)
    assert not get_syncs(G)


def test_add_artificial_source_sync():
    G = nx.DiGraph([(0, 1), (1, 2), (3, 2), (4, 1), (2, 5)])
    add_artificial_source_sync(G)
    assert get_sources(G) == ['artif_source']
    assert get_syncs(G) == ['artif_sync']
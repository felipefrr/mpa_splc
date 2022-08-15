"""
Graph methods for Main Path Analysis.
"""
import networkx as nx
from copy import deepcopy

__all__ = [
    "compare_graphs",
    "get_syncs",
    "get_sources",
    "path_contain_edge",
    "convert_graph_to_dag"
]


def graph_comparison_helper(edge1: dict, edge2: dict) -> bool:
    """Checks if both edges have the same SPLC weight

    Parameters
    ----------
    edge1 : list
        A list of size two containing the source and target
        nodes of an edge.

    edge2 : list
        A list of size two containing the source and target
        nodes of an edge.

    Returns
    -------
    bool
        Return True if both edges have equal SPLC weight value.
    """
    return edge1["SPLC"] == edge2["SPLC"]


def compare_graphs(G1, G2) -> bool:
    """Checks if graph `G1` and `G2` are isomorphic,
    in other words, checks if they are equal, and
    their edge weights as well.

    Parameters
    ----------
    G1 : networkx.DiGraph

    G2 : networkx.DiGraph

    Returns
    -------
    bool
        Return True if graph `G1` and `G2` are equals.
    """
    return nx.is_isomorphic(G1, G2, edge_match=graph_comparison_helper)


def get_syncs(G) -> list:
    """Returns a list containing all the sync nodes in `G`.

    Parameters
    ----------
    G : networkx.DiGraph

    Returns
    -------
    list
        A list of zero or more nodes in the graph `G`.
    """
    return [node for node in G.nodes if G.out_degree(node) == 0]


def get_sources(G) -> list:
    """Returns a list containing all the source nodes in `G`.

    Parameters
    ----------
    G : networkx.DiGraph

    Returns
    -------
    list
        A list of zero or more nodes in the graph `G`.
    """
    return [node for node in G.nodes if G.in_degree(node) == 0]


def path_contain_edge(edge: list, path: list) -> bool:
    """Returns True if and only if `path` contain the `edge`.

    Parameters
    ----------
    edge : list
        A list containing the head and the tail of edge.

    path : list
        A list of lists containing paths.

    Returns
    -------
    bool
        Whether the given edge is contained by the given path.

    Notes
    -----
    This function creates a map with an anonymous function that takes each sub-list of size
    two in `path` and compares with `edge`. The map is wrapped inside an `any` function that
    checks if there was any `True` value.
    """
    return any(map(lambda x: path[x:x + len(edge)] == edge, range(len(path) - len(edge) + 1)))


def convert_graph_to_dag(G, weight='pln_date'):
    """ Convert the digraph with cycles to an Acyclic Direct Graph (DAG)

    The heuristic in this function is to reverse the edge with the lowest weight of the cycle
    if possible, otherwise remove it.

    Parameters
    ----------
    G : networkx.DiGraph

    weight : str
        The edge attribute to be considered.

    Returns
    -------
    networkx.DiGraph
        The DAG made out of G.

    Notes
    -----
        The default value for weight is `pln_date` because it considers the configuration of
        our personal graph.
    """
    number_of_cycles = len(list(nx.simple_cycles(G)))
    while not nx.is_directed_acyclic_graph(G):
        cycle = next(nx.simple_cycles(G))
        edges = [(cycle[-1], cycle[0])]
        scores = [(G[cycle[-1]][cycle[0]][weight])]
        for i, j in zip(cycle[:-1], cycle[1:]):
            edges.append((i, j))
            scores.append(G[i][j][weight])

        i, j = edges[scores.index(min(scores))]

        # Create a copy of the Graph to check whether it will remove or reverse the edge
        copy_of_G = deepcopy(G)
        copy_of_G.remove_edge(i, j)
        copy_of_G.add_edge(j, i)

        # Check if we reverse the edge it still preserves the acyclicity
        new_num_of_cycles = len(list(nx.simple_cycles(copy_of_G)))
        if new_num_of_cycles < number_of_cycles:
            G.add_edge(j, i, weight=min(scores))
        G.remove_edge(i, j)
        number_of_cycles = new_num_of_cycles
    return G

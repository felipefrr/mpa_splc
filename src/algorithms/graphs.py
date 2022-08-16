"""
Graph methods for Main Path Analysis.
"""
import networkx as nx

__all__ = [
    "compare_graphs",
    "get_syncs",
    "get_sources",
    "path_contain_edge",
    "remove_cycles"
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


def remove_cycles(G, weight='pln_date'):
    """ Remove the cycles of the digraph to convert it an Acyclic Direct Graph (DAG)

    The heuristic in this function is to remove the edge with the lowest weight of the cycle.

    Parameters
    ----------
    G : networkx.DiGraph

    weight : str
        The edge attribute to be considered.

    Returns
    -------
    None

    Notes
    -----
        The default value for weight is `pln_date` because it considers the configuration of
        our personal graph.
    """
    while not nx.is_directed_acyclic_graph(G):
        cycle = next(nx.simple_cycles(G))
        edges = [(cycle[-1], cycle[0])]
        scores = [(G[cycle[-1]][cycle[0]][weight])]

        for head, tail in zip(cycle[:-1], cycle[1:]):
            edges.append((head, tail))
            scores.append(G[head][tail][weight])

        head, tail = edges[scores.index(min(scores))]
        G.remove_edge(head, tail)

"""
Graph methods for Main Path Analysis.
"""
# import networkx as nx

__all__ = [
    "get_syncs",
    "get_sources",
    "path_contain_edge"
]


def get_syncs(G):
    """Returns a list containing all the sync nodes in `G`.

    Parameters
    ----------
    G : graph
        A NetworkX graph.

    Returns
    -------
    list
        A list of zero or more nodes in the graph `G`.
    """
    return [node for node in G.nodes if G.out_degree(node) == 0]


def get_sources(G):
    """Returns a list containing all the source nodes in `G`.

    Parameters
    ----------
    G : graph
        A NetworkX graph.

    Returns
    -------
    list
        A list of zero or more nodes in the graph `G`.
    """
    return [node for node in G.nodes if G.in_degree(node) == 0]


def path_contain_edge(edge, path):
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

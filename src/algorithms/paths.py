"""
Path finding methods for Main Path Analysis.
"""
import warnings
import networkx as nx

__all__ = [
    "main_path",
]


def main_path(G, source="source", target="sync", weight="SPLC", method="longest"):
    """Compute the main path in the graph

    If `G` has edges with `SPLC` attribute the edge data are used as
    weight values.

    Parameters
    ----------
    G : NetworkX digraph
        A weighted directed acyclic graph (DAG)

    source : node, optional
        Starting node for path. If not specified, compute main
        path for `source` node.

    target : node, optional
        Ending node for path. If not specified, compute main
        path `sync` node.

    weight : string, optional (default = 'SPLC')
        If a string, use this edge attribute as the edge weight.
        If None, every edge has weight/distance/cost 1.

    method : string, optional (default = 'longest')
        The algorithm to use to compute the path.
        Supported options: 'longest', 'shortest'.
        Other inputs produce a ValueError.

    Returns
    -------
    path: list
        The main path include both the source and target in the path.
        Return a single list of nodes in a path from the source to the target.

    Raises
    ------
    ValueError
        If `method` is not among the supported options.
        If graph don't have the `weight` attribute

    Notes
    -----
    There may be more than one shortest path between a source and target.
    This returns only one of them.

    """
    if method not in ("longest", "shortest"):
        # so we don't need to check in each branch later
        raise ValueError(f"method not supported: {method}")

    if not nx.is_weighted(G, weight=weight):
        warnings.warn("weight = {} not found, proceeding with default weight = 1".format(weight))

    # Find main source-target path.
    if method == "longest":
        path = nx.dag_longest_path(G, weight=weight)
    elif method == "shortest":
        path = nx.dijkstra_path(G, source=source, target=target)
    else:
        path = []

    return path

"""
Path finding methods for Main Path Analysis.
"""
import warnings
import networkx as nx

from networkx.utils import pairwise

__all__ = [
    "main_path",
    "dag_longest_path_length",
    "prepare_for_dijkstra"
]


def main_path(G, source="source", weight="SPLC", method="longest"):  # pragma: no cover
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
    The longest method uses topological ordering therefore it calculates the
    global longest path.
    In the second method the longest paths correspond to the shortest paths in the
    negative graph where all edge weights are negated.

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
        path = nx.bellman_ford(G, source=source, weight=weight)
    else:
        path = []

    return path


def prepare_for_dijkstra(G):
    """Prepare G to be use in dijkstra path finding by negating all its
    edges weight values.

        Parameters
        ----------
        G : NetworkX digraph
            A weighted directed acyclic graph (DAG)

        Returns
        -------
            None

        Notes
        -----
        The longest distance problem on graph G is equivalent to the shortest
        distance problem in a transformed graph G'=-G, i.e., the sign of each
        edge weight is reversed.
    """
    for edge in list(G.edges()):
        source, target = edge
        G[source][target]["SPLC"] *= -1


def dag_longest_path_length(G, path, weight="weight", default_weight=1):  # pragma: no cover
    """Returns the longest path length in a DAG

    Parameters
    ----------
    G : NetworkX DiGraph
        A directed acyclic graph (DAG)

    path: list
        The list contaning the nodes of the path to be traversed

    weight : string, optional
        Edge data key to use for weight

    default_weight : int, optional
        The weight of edges that do not have a weight attribute

    Returns
    -------
    int
        Longest path length
    """
    path_length = 0
    if not path:
        return path_length
    for (u, v) in pairwise(path):
        path_length += G[u][v].get(weight, default_weight)

    return path_length

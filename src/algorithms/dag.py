"""
Directed Acyclic Graph methods for Main Path Analysis.
"""
import networkx as nx

__all__ = [
    "compare_graphs",
    "get_syncs",
    "get_sources",
    "path_contain_edge",
    "remove_cycles",
    "add_artificial_source_sync",
    "simplify",
    "remove_anomalies"
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


def remove_cycles(G, weight="pln_date") -> list:
    """ Remove the cycles of the digraph to convert it an Acyclic Direct Graph (DAG)

    The heuristic in this function is to remove the edge with the lowest weight of the cycle.

    Parameters
    ----------
    G : networkx.DiGraph

    weight : str
        The edge attribute to be considered.

    Returns
    -------
    list
        The list of edges removed

    Notes
    -----
        The default value for weight is `pln_date` because it considers the configuration of
        our personal graph.
    """
    edges_removed = []
    while not nx.is_directed_acyclic_graph(G):
        cycle = next(nx.simple_cycles(G))
        edges = [(cycle[-1], cycle[0])]
        scores = [(G[cycle[-1]][cycle[0]][weight])]

        for head, tail in zip(cycle[:-1], cycle[1:]):
            edges.append((head, tail))
            scores.append(G[head][tail][weight])

        head, tail = edges[scores.index(min(scores))]
        G.remove_edge(head, tail)
        edges_removed.append((head, tail))
    return edges_removed


def add_artificial_source_sync(G):  # pragma: no cover
    """ Add two artificial vertices, `source` and `sync` vertex such that reduces
    the graph set of sources to a single source and syncs to a single sync vertex.

    Parameters
    ----------
    G : networkx.DiGraph

    Returns
    -------
    None

    Notes
    -----
        The resulting graph is always connected because previous connected components are
        joined at source and sink.
    """
    if nx.is_empty(G):
        return

    sources = get_sources(G)
    syncs = get_syncs(G)

    for source in sources:
        G.add_edge("source", source)

    for sync in syncs:
        G.add_edge(sync, "sync")


def simplify(G) -> nx.DiGraph:  # pragma: no cover
    """ Simplifies `G` by deleting the vertices and arcs that do not belong to any cycle..

    Parameters
    ----------
    G : networkx.DiGraph

    Returns
    -------
     H : networkx.DiGraph
        Returns the simplified version of `G`

    Notes
    -----
        It aims to decrease the scale of the graph, especially when `G` is sparse.
    """
    if nx.is_empty(G):
        return None

    H = G.copy()

    nodes_to_remove = [node for node in H.nodes if H.in_degree(node) == 0 or H.out_degree(node) == 0]

    for node in nodes_to_remove:
        H.remove_node(node)

    return H


def remove_anomalies(G, weight="pln_date") -> int:  # pragma: no cover
    """ Given two edges remove the edges to future nodes, i.e., given `e1` and `e2`,
    with `e1[weight]` < `e2[weight]`.


    Parameters
    ----------
    G : networkx.DiGraph

    weight : str
        The edge attribute to be considered.

    Returns
    -------
        int
        Number of anomalies removed

    Notes
    -----
        This anomalies could be references identified during the examination process and
        represents the prior art used for the various office actions that take
        place during prosecution.
    """
    edges_removed = 0
    edges = list(G.edges())
    for edge in edges:
        source, target = edge
        if G.nodes[source] and G.nodes[target]:
            if G.nodes[source][weight] < G.nodes[target][weight]:
                G.remove_edge(source, target)
                edges_removed += 1

    return edges_removed

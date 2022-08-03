"""
Weight calculation methods for Main Path Analysis.
"""
import networkx as nx

from src.algorithms.graphs import path_contain_edge


def calculate_spc(G, sources, syncs):
    """Calculate the edge weight SPC for all edges in `G` and stores
    its value in a hash inside `G where its key is the edge and value
    is the `SPC` calculated.

    Parameters
    ----------
    G: NetworkX graph

    sources: list
             Source nodes list

    syncs:  list
            Sync nodes list

    Returns
    ----------
    None

    """
    edges = list(map(list, G.edges()))
    all_paths = []
    for source in sources:
        for sync in syncs:
            paths = (list(nx.all_simple_paths(G, source, sync)))
            all_paths += paths if paths else []

    for edge in edges:
        spc = 0
        for path in all_paths:
            spc += 1 if path_contain_edge(edge, path) else 0
            G[edge[0]][edge[1]]["SPC"] = spc


def calculate_splc_fast(G, sources, syncs):
    """Calculate the edge weight SPLC for all edges in `G` and stores
    its values in a hash inside `G where its key is the edge and value
    is the `SPLC` calculated. This version is slightly optimized because
    stores all paths containing the edge inside a set.

        Parameters
        ----------
        G: NetworkX graph

        sources: list
                 Source nodes list

        syncs:  list
                Sync nodes list

        Returns
        ----------
        None

        """
    edges = list(map(list, G.edges()))
    all_paths = []

    for source in sources:
        for sync in syncs:
            paths = (list(nx.all_simple_paths(G, source, sync)))
            all_paths += paths if paths else []

    for edge in edges:
        all_paths_containing_edge = set()
        for path in all_paths:
            if path_contain_edge(edge, path):
                edge_head = edge[0]
                head_path_start_index = 0

                while edge_head != path[head_path_start_index]:
                    head_path_start_index += 1

                for index in range(head_path_start_index, -1, -1):
                    all_paths_containing_edge.add("".join(path[index:]))

        G[edge[0]][edge[1]]["SPLC"] = len(all_paths_containing_edge)


def calculate_splc(G, syncs):
    """Calculate the edge weight SPLC for all edges in `G` and stores
    its values in a hash inside `G where its key is the edge and value
    is the `SPLC` calculated.

        Parameters
        ----------
        G: NetworkX graph

        syncs:  list
                Sync nodes list

        Returns
        ----------
        None

        """
    edges = list(map(list, G.edges()))

    for edge in edges:
        edge_head = edge[0]
        edge_tail = edge[1]
        ancestors = list(nx.ancestors(G, edge_head))
        paths_containing_edge = 0
        for ancestor in ancestors:
            for sync in syncs:
                paths = list(nx.all_simple_paths(G, ancestor, sync))
                for path in paths:
                    if path_contain_edge(edge, path):
                        paths_containing_edge += 1

        for sync in syncs:
            paths = list(nx.all_simple_paths(G, edge_head, sync))
            for path in paths:
                if path_contain_edge(edge, path):
                    paths_containing_edge += 1

        G[edge_head][edge_tail]["SPLC"] = paths_containing_edge

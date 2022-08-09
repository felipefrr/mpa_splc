"""
Node weight calculation methods for Main Path Analysis.
"""
import networkx as nx

__all__ = [
    "calculate_n_all_minus",
    "calculate_n_plus",
]


def calculate_n_all_minus(G, node: str):
    """Calculate the node Nall⁻ weight for the given node and stores
        its value in a hash inside `G` where the key is `Nall-` and value
        is the `Nall-` calculated.

        Parameters
        ----------
        G: NetworkX graph

        node:  str
               The starting node label

        Returns
        ----------
        None

        Notes
        ----------
        It is important to note that this function uses dynamic programming
        to calculate the values of `Nall-`, and for it to work correctly, its
        calls must occur in topological order.
    """
    G.nodes[node]["Nall-"] = 1
    for predecessor in G.predecessors(node):
        G.nodes[node]["Nall-"] += G.nodes[predecessor]["Nall-"]
    print(G.nodes[node]["Nall-"])


def calculate_n_plus(G, node: str, syncs: list):
    """Calculate the node Nall⁺ weight for the given node and stores
        its value in a hash inside `G` where the key is `Nall+` and value
        is the `Nall+` calculated.

        Parameters
        ----------
        G: NetworkX graph

        node:  str
               The starting node label

        Returns
        ----------
        None

        Notes
        ----------
        It is important to note that this function uses dynamic programming
        to calculate the values of `N+`, and for it to work correctly, its
        calls must occur in reverse topological order.

        The sync node checking can be improved if we use an indicator flag
        in the sync nodes.

        Later on, we will notice that artificially creating a global source and
        sync node, connecting them with, respectively, all source nodes and
        sync nodes will help us find the main path more efficiently.
    """
    if node in syncs:
        G.nodes[node]["N+"] = 1
        return

    G.nodes[node]["N+"] = G.nodes.get("N+", 0)

    for successor in G.successors(node):
        G.nodes[node]["N+"] += G.nodes[successor]["N+"]
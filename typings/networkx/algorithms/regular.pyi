"""
This type stub file was generated by pyright.
"""

from networkx.utils import not_implemented_for

"""Functions for computing and verifying regular graphs."""
__all__ = ["is_regular", "is_k_regular", "k_factor"]
def is_regular(G): # -> bool:
    """Determines whether the graph ``G`` is a regular graph.

    A regular graph is a graph where each vertex has the same degree. A
    regular digraph is a graph where the indegree and outdegree of each
    vertex are equal.

    Parameters
    ----------
    G : NetworkX graph

    Returns
    -------
    bool
        Whether the given graph or digraph is regular.

    """
    ...

@not_implemented_for("directed")
def is_k_regular(G, k): # -> bool:
    """Determines whether the graph ``G`` is a k-regular graph.

    A k-regular graph is a graph where each vertex has degree k.

    Parameters
    ----------
    G : NetworkX graph

    Returns
    -------
    bool
        Whether the given graph is k-regular.

    """
    ...

@not_implemented_for("directed")
@not_implemented_for("multigraph")
def k_factor(G, k, matching_weight=...):
    """Compute a k-factor of G

    A k-factor of a graph is a spanning k-regular subgraph.
    A spanning k-regular subgraph of G is a subgraph that contains
    each vertex of G and a subset of the edges of G such that each
    vertex has degree k.

    Parameters
    ----------
    G : NetworkX graph
      Undirected graph

    matching_weight: string, optional (default='weight')
       Edge data key corresponding to the edge weight.
       Used for finding the max-weighted perfect matching.
       If key not found, uses 1 as weight.

    Returns
    -------
    G2 : NetworkX graph
        A k-factor of G

    References
    ----------
    .. [1] "An algorithm for computing simple k-factors.",
       Meijer, Henk, Yurai Núñez-Rodríguez, and David Rappaport,
       Information processing letters, 2009.
    """
    class LargeKGadget:
        ...
    
    
    class SmallKGadget:
        ...
    
    


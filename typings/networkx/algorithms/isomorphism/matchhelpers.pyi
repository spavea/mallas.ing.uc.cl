"""
This type stub file was generated by pyright.
"""

"""Functions which help end users define customize node_match and
edge_match functions to use during isomorphism checks.
"""
__all__ = ["categorical_node_match", "categorical_edge_match", "categorical_multiedge_match", "numerical_node_match", "numerical_edge_match", "numerical_multiedge_match", "generic_node_match", "generic_edge_match", "generic_multiedge_match"]
def copyfunc(f, name=...): # -> FunctionType:
    """Returns a deepcopy of a function."""
    ...

def allclose(x, y, rtol=..., atol=...): # -> bool:
    """Returns True if x and y are sufficiently close, elementwise.

    Parameters
    ----------
    rtol : float
        The relative error tolerance.
    atol : float
        The absolute error tolerance.

    """
    ...

categorical_doc = ...
def categorical_node_match(attr, default): # -> (data1: Unknown, data2: Unknown) -> Unknown:
    ...

categorical_edge_match = ...
def categorical_multiedge_match(attr, default): # -> (datasets1: Unknown, datasets2: Unknown) -> bool:
    ...

tmpdoc = ...
tmpdoc = ...
numerical_doc = ...
def numerical_node_match(attr, default, rtol=..., atol=...): # -> (data1: Unknown, data2: Unknown) -> bool:
    ...

numerical_edge_match = ...
def numerical_multiedge_match(attr, default, rtol=..., atol=...): # -> (datasets1: Unknown, datasets2: Unknown) -> bool:
    ...

tmpdoc = ...
tmpdoc = ...
generic_doc = ...
def generic_node_match(attr, default, op): # -> (data1: Unknown, data2: Unknown) -> Unknown:
    ...

generic_edge_match = ...
def generic_multiedge_match(attr, default, op): # -> (datasets1: Unknown, datasets2: Unknown) -> bool:
    """Returns a comparison function for a generic attribute.

    The value(s) of the attr(s) are compared using the specified
    operators. If all the attributes are equal, then the constructed
    function returns True. Potentially, the constructed edge_match
    function can be slow since it must verify that no isomorphism
    exists between the multiedges before it returns False.

    Parameters
    ----------
    attr : string | list
        The edge attribute to compare, or a list of node attributes
        to compare.
    default : value | list
        The default value for the edge attribute, or a list of
        default values for the dgeattributes.
    op : callable | list
        The operator to use when comparing attribute values, or a list
        of operators to use when comparing values for each attribute.

    Returns
    -------
    match : function
        The customized, generic `edge_match` function.

    Examples
    --------
    >>> from operator import eq
    >>> from math import isclose
    >>> from networkx.algorithms.isomorphism import generic_node_match
    >>> nm = generic_node_match("weight", 1.0, isclose)
    >>> nm = generic_node_match("color", "red", eq)
    >>> nm = generic_node_match(["weight", "color"], [1.0, "red"], [isclose, eq])
    ...

    """
    ...

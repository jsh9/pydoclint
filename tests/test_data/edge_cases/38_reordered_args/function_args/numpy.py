# The docstrings list the arguments in a different order from the signatures.
# The signatures have no types; only the docstrings do.


def wrongOrder(b, a) -> None:
    """
    Only the order is wrong.

    Parameters
    ----------
    a : int
        A.
    b : str
        B.
    """


def wrongOrderAndDefault(b=1, a=2) -> None:
    """
    The order is wrong, and so is the documented default of `b`.

    Parameters
    ----------
    a : int, default=2
        A.
    b : int, default=5
        B.
    """

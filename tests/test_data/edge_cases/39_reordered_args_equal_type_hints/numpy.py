from typing import Dict


def f(b: Dict[str, int], a: int) -> None:
    """
    The order is wrong. The type of `b` is written with different spacing, but
    it's the same type.

    Parameters
    ----------
    a : int
        A.
    b : Dict[str,int]
        B.
    """

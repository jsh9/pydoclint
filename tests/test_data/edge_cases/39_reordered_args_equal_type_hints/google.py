from typing import Dict


def f(b: Dict[str, int], a: int) -> None:
    """
    The order is wrong, so this gets DOC104. The type of `b` is written with
    different spacing in the docstring, but it's the same type, so this must
    not get DOC105 (in the right order, it gets nothing).

    Args:
        a (int): A.
        b (Dict[str,int]): B.
    """

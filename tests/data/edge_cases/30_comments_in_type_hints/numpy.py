"""Test case for noqa comments in class attribute type hints in numpy style docstrings."""


def regular_function(
        param1: str,
        param2: int = 42,
        param3: float = 3.14,
        param4: str = "foo",
) -> bool:
    """A regular function with parameters.

    Parameters
    ----------
    param1 : str  # noqa: E501
        First parameter with noqa comment.
    param2 : int, default=42#noqa:F401
        Second parameter with no-space noqa comment.
    param3 : float, default=3.14
        Third parameter with no-space noqa comment.
    param4 : str, default='foobar'  # noqa: E501
        Fourth parameter with no-space noqa comment.

    Returns
    -------
    bool
        The result.
    """
    return True


class TestClass:
    """Class with attributes that have noqa comments in type hints.

    Attributes
    ----------
    attr1 : str # noqa: E501
        Regular noqa comment in type hint.
    attr2 : int, default=42#noqa:E501
        No-space noqa comment in type hint.
    attr3 : float, default=3.14  #  NOQA  :  E501
        Spaced and uppercase noqa comment.
    attr4 : bool, default=True # noqa: E501,W503
        Multiple rule codes in noqa.
    attr5 : list, default=[] # this is not noqa
        Regular comment that should remain.
    attr6 : dict, default={} # noqa: F401
        Complex type with noqa comment.
    """

    attr1: str
    attr2: int = 42
    attr3: float = 3.14
    attr4: bool = True
    attr5: list = []
    attr6: dict = {}

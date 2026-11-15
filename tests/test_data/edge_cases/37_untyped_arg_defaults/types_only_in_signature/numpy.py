# The signatures have types; the docstrings only give the defaults


def correctDefault(x: int = 3) -> None:
    """
    The documented default is right.

    Parameters
    ----------
    x : , default=3
        The x value.
    """


def wrongDefault(x: int = 3) -> None:
    """
    The documented default is wrong.

    Parameters
    ----------
    x : , default=4
        The x value.
    """


def missingDefault(x: int = 3) -> None:
    """
    The default is not documented.

    Parameters
    ----------
    x
        The x value.
    """


def spuriousDefault(x: int) -> None:
    """
    A default is documented, but the argument doesn't have one.

    Parameters
    ----------
    x : , default=3
        The x value.
    """

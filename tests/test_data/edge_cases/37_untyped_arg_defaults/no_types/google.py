# No types anywhere; the docstrings only give the defaults


def correctDefault(value=3) -> None:
    """
    The documented default is right.

    Args:
        value (, default=3): A value.
    """


def wrongDefault(value=3) -> None:
    """
    The documented default is wrong.

    Args:
        value (, default=4): A value.
    """

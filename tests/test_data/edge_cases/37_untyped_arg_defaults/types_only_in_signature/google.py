# The signatures have types; the docstrings only give the defaults


def correctDefault(x: int = 3) -> None:
    """
    The documented default is right.

    Args:
        x (, default=3): The x value.
    """


def wrongDefault(x: int = 3) -> None:
    """
    The documented default is wrong.

    Args:
        x (, default=4): The x value.
    """

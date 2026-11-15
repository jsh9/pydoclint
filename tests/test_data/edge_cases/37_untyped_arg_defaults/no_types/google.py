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


def missingDefault(value=3) -> None:
    """
    The default is not documented.

    Args:
        value: A value.
    """


def spuriousDefault(value) -> None:
    """
    A default is documented, but the argument doesn't have one.

    Args:
        value (, default=3): A value.
    """

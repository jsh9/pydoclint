# The signatures have no types; only the docstrings do


def correctDefault(alpha=0.05) -> None:
    """
    The documented default is right.

    Args:
        alpha (float, default=0.05): The alpha value.
    """


def wrongDefault(alpha=0.05) -> None:
    """
    The documented default is wrong.

    Args:
        alpha (float, default=0.5): The alpha value.
    """


def missingDefault(alpha=0.05) -> None:
    """
    The default is not documented.

    Args:
        alpha (float): The alpha value.
    """


def extraDefault(alpha) -> None:
    """
    A default is documented, but the argument doesn't have one.

    Args:
        alpha (float, default=0.05): The alpha value.
    """


def freeFormType(values=None) -> None:
    """
    The type is not valid Python, but the documented default is right.

    Args:
        values (array-like of shape (n,), default=None): The values.
    """

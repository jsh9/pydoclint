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


def spuriousDefault(alpha) -> None:
    """
    A default is documented, but the argument doesn't have one.

    Args:
        alpha (float, default=0.05): The alpha value.
    """


def freeFormCorrectDefault(values=None) -> None:
    """
    The type is not valid Python, and the documented default is right.

    Args:
        values (array-like of shape (n,), default=None): The values.
    """


def freeFormWrongDefault(values=None) -> None:
    """
    The type is not valid Python, and the documented default is wrong.

    Args:
        values (array-like of shape (n,), default=[]): The values.
    """


def freeFormMissingDefault(values=None) -> None:
    """
    The type is not valid Python, and the default is not documented.

    Args:
        values (array-like of shape (n,)): The values.
    """


def freeFormSpuriousDefault(values) -> None:
    """
    The type is not valid Python, and a default is documented, but the
    argument doesn't have one.

    Args:
        values (array-like of shape (n,), default=None): The values.
    """

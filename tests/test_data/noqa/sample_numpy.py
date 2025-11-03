def funcDocstringComment(arg1: int, arg2: int) -> None:
    """Demonstrate docstring comment suppression.

    Parameters
    ----------
    arg1 : int
        Documented argument.
    """  # explanation noqa: doc101, doc103
    pass


def funcDefinitionComment(arg1: int, arg2: int) -> None:  # noqa: DOC103
    """Demonstrate definition line suppression.

    Parameters
    ----------
    arg1 : int
        Documented argument.
    """
    pass


def funcWithoutComment(arg1: int, arg2: int) -> None:
    """Docstring without suppression comments.

    Parameters
    ----------
    arg1 : int
        Documented argument.
    """
    pass

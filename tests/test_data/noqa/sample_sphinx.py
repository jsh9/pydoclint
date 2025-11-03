def funcDocstringComment(arg1: int, arg2: int) -> None:
    """Demonstrate docstring comment suppression.

    :param int arg1: Documented argument.

    """  # explanation noqa: doc101, doc103, E999 irrelevant
    pass


def funcDefinitionComment(arg1: int, arg2: int) -> None:  # noqa: DOC103 details
    """Demonstrate definition line suppression.

    :param int arg1: Documented argument.

    """
    pass


def funcWithoutComment(arg1: int, arg2: int) -> None:
    """Docstring without suppression comments.

    :param int arg1: Documented argument.

    """
    pass

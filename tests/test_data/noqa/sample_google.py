def funcDocstringComment(arg1: int, arg2: int) -> None:
    """Demonstrate docstring comment suppression.

    Args:
        arg1 (int): Documented argument.

    """  # explanation noqa: doc101, doc103, F401 trailing words
    pass


def funcDefinitionComment(arg1: int, arg2: int) -> None:  # noqa: DOC103 chatter
    """Demonstrate definition line suppression.

    Args:
        arg1 (int): Documented argument.

    """
    pass


def funcWithoutComment(arg1: int, arg2: int) -> None:
    """Docstring without suppression comments.

    Args:
        arg1 (int): Documented argument.

    """
    pass

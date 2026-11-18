# See https://github.com/jsh9/pydoclint/issues/343
from typing import Annotated, Literal


def returnAnnotatedHash() -> Annotated[int, "#x"]:
    """
    Return an Annotated int whose metadata contains ``#``.

    Returns:
        Annotated[int, "#x"]: A value.
    """
    return 1


def returnLiteralBracket() -> Literal['a]', 'b']:
    """
    Return a Literal string containing ``]``.

    Returns:
        Literal['a]', 'b']: A token.
    """
    return 'a]'


def returnMismatchedAnnotatedHash() -> Annotated[int, '#x']:
    """
    Return an Annotated int documented with the wrong return type.

    Returns:
        str: Wrong type.
    """
    return 1

# fmt: off
from __future__ import annotations

from typing import Literal


def func_1(arg1: Literal["foo"]) -> Literal["foo"]:
    """
    Test literal.

    Args:
        arg1 (Literal["foo"]): Arg 1

    Returns:
        Literal["foo"]: The literal string "foo".
    """
    return "foo"


def func_2(arg1: Literal['foo']) -> Literal['foo']:
    """
    Test literal.

    Args:
        arg1 (Literal['foo']): Arg 1

    Returns:
        Literal['foo']: The literal string "foo".
    """
    return "foo"


def func_3(arg1: Literal['foo']) -> tuple[Literal['foo'], Literal["bar"]]:
    """
    Test literal.

    Args:
        arg1 (Literal['foo']): Arg 1

    Returns:
        tuple[Literal['foo'], Literal["bar"]]: The literal strings 'foo' & "bar"
    """
    return 'foo', "bar"

# fmt: off

# This edge case comes from https://github.com/jsh9/pydoclint/issues/105

from __future__ import annotations

from typing import Literal


def func_1(arg1: Literal["foo"]) -> Literal["foo"]:
    """
    Test literal.

    Parameters
    ----------
    arg1 : Literal["foo"]
        Arg 1

    Returns
    -------
    Literal["foo"]
        The literal string "foo".
    """
    return "foo"


def func_2(arg1: Literal['foo']) -> Literal['foo']:
    """
    Test literal.

    Parameters
    ----------
    arg1 : Literal['foo']
        Arg 1

    Returns
    -------
    Literal['foo']
        The literal string 'foo'.
    """
    return "foo"


def func_3() -> tuple[Literal['foo'], Literal["bar"]]:
    """
    Test literal.

    Returns
    -------
    Literal['foo']
        The literal string 'foo'. And the quote style (single) must match
        the function signature.
    Literal["bar"]
        The literal string "bar". And the quote style (double) must match
        the function signature.
    """
    return "foo", 'bar'

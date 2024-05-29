# This edge case comes from: https://github.com/jsh9/pydoclint/issues/127

from __future__ import annotations

from typing import Iterable, Iterator


def f1(args: list):
    """ASDF

    Arguments
    ---------
    args: list
        args

    Yields
    ------
    args: Iterable
    """
    yield from args


def f2(args: list) -> Iterator[Iterable]:
    """ASDF

    Arguments
    ---------
    args: list
        args

    Yields
    ------
    args: Iterable
    """
    yield from args

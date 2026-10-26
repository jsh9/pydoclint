import collections.abc
import typing
import typing as t


def yieldAndReturn() -> collections.abc.Generator[int, None, str]:
    """Exercise qualified annotations.

    Check how the annotation controls yield and return documentation.

    :yields: A number.
    :ytype: int

    :returns: The final result.
    :rtype: str
    """
    ...


def shortGenerator() -> t.Generator[int, str]:
    """Exercise qualified annotations.

    Check how the annotation controls yield and return documentation.

    :yields: A number.
    :ytype: int
    """
    ...


async def asyncGenerator() -> typing.AsyncGenerator[int]:
    """Exercise qualified annotations.

    Check how the annotation controls yield and return documentation.

    :yields: A number.
    :ytype: int
    """
    ...


def iterator() -> collections.abc.Iterator[int]:
    """Exercise qualified annotations.

    Check how the annotation controls yield and return documentation.

    :yields: A number.
    :ytype: int
    """
    ...


def noneIterable() -> t.Iterable[None]:
    """Exercise qualified annotations.

    Check how the annotation controls yield and return documentation.
    """
    ...

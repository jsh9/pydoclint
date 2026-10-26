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
    yield 1
    return 'done'


def shortGenerator() -> t.Generator[int, str]:
    """Exercise qualified annotations.

    Check how the annotation controls yield and return documentation.

    :yields: A number.
    :ytype: int
    """
    yield 1


async def asyncGenerator() -> typing.AsyncGenerator[int]:
    """Exercise qualified annotations.

    Check how the annotation controls yield and return documentation.

    :yields: A number.
    :ytype: int
    """
    yield 1


def iterator() -> collections.abc.Iterator[int]:
    """Exercise qualified annotations.

    Check how the annotation controls yield and return documentation.

    :yields: A number.
    :ytype: int
    """
    yield 1


def noneIterable() -> t.Iterable[None]:
    """Exercise qualified annotations.

    Check how the annotation controls yield and return documentation.
    """
    yield None

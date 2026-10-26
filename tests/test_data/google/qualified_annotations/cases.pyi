import collections.abc
import typing
import typing as t


def yieldAndReturn() -> collections.abc.Generator[int, None, str]:
    """Exercise qualified annotations.

    Check how the annotation controls yield and return documentation.

    Yields:
        int: A number.

    Returns:
        str: The final result.
    """
    ...


def shortGenerator() -> t.Generator[int, str]:
    """Exercise qualified annotations.

    Check how the annotation controls yield and return documentation.

    Yields:
        int: A number.
    """
    ...


async def asyncGenerator() -> typing.AsyncGenerator[int]:
    """Exercise qualified annotations.

    Check how the annotation controls yield and return documentation.

    Yields:
        int: A number.
    """
    ...


def iterator() -> collections.abc.Iterator[int]:
    """Exercise qualified annotations.

    Check how the annotation controls yield and return documentation.

    Yields:
        int: A number.
    """
    ...


def noneIterable() -> t.Iterable[None]:
    """Exercise qualified annotations.

    Check how the annotation controls yield and return documentation.
    """
    ...

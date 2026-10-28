from abc import abstractmethod
from typing import Generator, AsyncGenerator, Iterator, AsyncIterator, Iterable, AsyncIterable


def generator() -> Generator[int]:
    """Yield a number.

    Yields
    ------
    int
        A value.
    """
    yield 1


async def asyncGenerator() -> AsyncGenerator[int]:
    """Yield a number.

    Yields
    ------
    int
        A value.
    """
    yield 1


def iterator() -> Iterator[int]:
    """Yield a number.

    Yields
    ------
    int
        A value.
    """
    yield 1


async def asyncIterator() -> AsyncIterator[int]:
    """Yield a number.

    Yields
    ------
    int
        A value.
    """
    yield 1


def iterable() -> Iterable[int]:
    """Yield a number.

    Yields
    ------
    int
        A value.
    """
    yield 1


async def asyncIterable() -> AsyncIterable[int]:
    """Yield a number.

    Yields
    ------
    int
        A value.
    """
    yield 1

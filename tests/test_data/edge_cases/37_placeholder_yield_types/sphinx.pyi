from abc import abstractmethod
from typing import Generator, Iterator


def returnsOnly() -> Iterator[int]:
    """Preserve existing section requirements.

    :returns: A value.
    :rtype: Iterator[int]
    """
    ...


def missingYields() -> Generator[int]:
    """Preserve existing section requirements.

    """
    ...


def nonGenerator() -> None:
    """Preserve existing section requirements.

    :yields: A value.
    :ytype: int
    """
    ...


def noneYield() -> Generator[None]:
    """Preserve existing section requirements.

    :yields: A value.
    :ytype: None
    """
    ...

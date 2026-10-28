from abc import abstractmethod
from typing import Generator, Iterator


def returnsOnly() -> Iterator[int]:
    """Preserve existing section requirements.

    Returns:
        Iterator[int]: A value.
    """
    ...


def missingYields() -> Generator[int]:
    """Preserve existing section requirements.

    """
    ...


def nonGenerator() -> None:
    """Preserve existing section requirements.

    Yields:
        int: A value.
    """
    ...


def noneYield() -> Generator[None]:
    """Preserve existing section requirements.

    Yields:
        None: A value.
    """
    ...

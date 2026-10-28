# Each function here has a "qualified" return annotation: the type name is
# reached through a module or a module alias, as in `typing.Generator[...]`,
# `collections.abc.Iterator[...]`, or `t.Iterable[...]` after
# `import typing as t`.
#
# The other kind is an "unqualified" (bare) annotation: the name is imported
# directly, as in `from typing import Generator`, and used as `Generator[...]`.
#
# pydoclint recognizes both kinds by looking only at the last name, without
# resolving imports. A renamed name, as in `from typing import Iterator as It`,
# is not recognized, because its last name is `It`.

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

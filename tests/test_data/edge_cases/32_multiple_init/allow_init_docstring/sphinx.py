from __future__ import annotations

from typing import overload


class Example:
    """Example class docstring."""

    @overload
    def __init__(self, value: str) -> None:
        """Incorrect docstring that should be ignored.

        :param wrong: This argument does not exist in the signature.
        :type wrong: int
        """

    def __init__(self, value: str, size: int) -> None:
        """Actual implementation docstring.

        :param value: Primary value.
        :param size: Size of something important.
        :type value: str
        :type size: int
        """

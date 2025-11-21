from __future__ import annotations

from typing import overload


class Example:
    """Example class docstring."""

    @overload
    def __init__(self, value: str) -> None:
        """Incorrect docstring that should be ignored.

        Parameters
        ----------
        wrong : int
            This argument does not exist in the signature.
        """

    def __init__(self, value: str, size: int) -> None:
        """Actual implementation docstring.

        Parameters
        ----------
        value : str
            Primary value.
        size : int
            Size of something important.
        """

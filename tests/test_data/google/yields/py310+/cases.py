# This can be merged into the parent folder after Py39 support is dropped.
# Because Python 3.9 does not suport match-case syntax.

from typing import Iterable


class A:
    def __init__(self, arg1):
        self.data = arg1

    def func10(self, arg0: bool) -> Iterable[int]:
        """
        There should be a DOC402 violation for this function

        Args:
            arg0 (bool): Arg 0

        Raises:
            ValueError: When there is a value error
        """
        for i in range(10):
            match i:
                case [0, 1]:
                    yield i
                case [2, 3]:
                    yield i + 1
                case _:
                    raise ValueError('Hello world')

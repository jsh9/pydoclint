from __future__ import annotations

from typing import overload

# This case comes from: https://github.com/jsh9/pydoclint/issues/255
class FooWrite(SomeObject):
    """
    The Foo write class.

    :param bar: Description of bar.
    :param baz: Description of baz.
    :type bar: str | None
    :type baz: int | None
    :raises ValueError: If both bar and baz are None.
    """

    @overload
    def __init__(self, bar: None, baz: None) -> NoReturn: ...

    @overload
    def __init__(self, bar: str | None, baz: int | None) -> None: ...

    def __init__(self, bar: str | None, baz: int | None) -> None:
        if bar is None and baz is None:
            raise ValueError

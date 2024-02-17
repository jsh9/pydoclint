import ast
from typing import List

import pytest

from pydoclint.utils.generic import collectFuncArgs, specialEqual, stripQuotes

src1 = """
def func1(
        arg1: int, *,
        arg2: str, arg3: bool,
        **kwargs) -> float:
    return 2.0
"""

expected1 = ['arg1', 'arg2', 'arg3', '**kwargs']

src2 = """
def func2(*, arg1,
        arg2, arg3,
            **kwargs):
    pass
"""

expected2 = ['arg1', 'arg2', 'arg3', '**kwargs']

src3 = """
def func3(arg1,
          arg2, *args,
          **kwargs):
    print(2)
"""

expected3 = ['arg1', 'arg2', '*args', '**kwargs']

src4 = """
def func4(*args):
    print(2)
"""

expected4 = ['*args']

src5 = """
def func5(**kwargs):
    print(2)
"""

expected5 = ['**kwargs']

src6 = """
def func6(*, arg1, arg2):
    print(2)
"""

expected6 = ['arg1', 'arg2']


@pytest.mark.parametrize(
    'src, expected',
    [
        (src1, expected1),
        (src2, expected2),
        (src3, expected3),
        (src4, expected4),
        (src5, expected5),
        (src6, expected6),
    ],
)
def testCollectFuncArgs(src: str, expected: List[str]) -> None:
    tree = ast.parse(src)
    out = collectFuncArgs(tree.body[0])
    assert [_.arg for _ in out] == expected


@pytest.mark.parametrize(
    'string, expected',
    [
        ('"Hello" \'world\'!', 'Hello world!'),
        (
            '"Hello" and "Goodbye", but Literal["This"] remains untouched',
            'Hello and Goodbye, but Literal["This"] remains untouched',
        ),
        ('Literal["abc", \'def\']', 'Literal["abc", \'def\']'),
        (
            'Union["MyClass", Literal["abc", "def"]]',
            'Union[MyClass, Literal["abc", "def"]]',
        ),
        ('Optional["MyClass"]', 'Optional[MyClass]'),
        ('Optional[MyClass]', 'Optional[MyClass]'),
    ],
)
def testStripQuotes(string: str, expected: str) -> None:
    assert stripQuotes(string) == expected


@pytest.mark.parametrize(
    'str1, str2, expected',
    [
        ('', '', True),  # truly equal
        ('"', '"', True),  # truly equal
        ("'", "'", True),  # truly equal
        ('"', "'", True),
        ('Hello" world\' 123', 'Hello" world\' 123', True),  # truly equal
        ('Hello" world\' 123', "Hello' world' 123", True),
        ('Hello" world\' 123', 'Hello\' world" 123', True),
        ('Hello" world\' 123', "Hello' world` 123", False),
        ('Hello" world\' 123', 'Hello\' world" 1234', False),
    ],
)
def testSpecialEqual(str1: str, str2: str, expected: bool) -> None:
    assert specialEqual(str1, str2) == expected

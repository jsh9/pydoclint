import ast
from typing import List, Optional

import pytest

from pydoclint.utils.generic import collectFuncArgs, isPropertyMethod

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


srcProperty1 = """
class A:
    def method1(self):
        pass
"""

srcProperty2 = """
class A:
    @property
    def method1(self):
        pass
"""

srcProperty3 = """
# pydoclint only does static code analysis in order to achieve fast speed.
# If users rename built-in decorator names (such as `property`), pydoclint
# will not recognize it.

hello_world = property

class A:
    @hello_world
    def method1(self):
        pass
"""


@pytest.mark.parametrize(
    'src, expected',
    [
        (srcProperty1, False),
        (srcProperty2, True),
        (srcProperty3, False),
    ],
)
def testIsPropertyMethod(src: str, expected: bool) -> None:
    def getMethod1(tree_: ast.AST) -> Optional[ast.FunctionDef]:
        for node_ in ast.walk(tree_):
            if isinstance(node_, ast.FunctionDef) and node_.name == 'method1':
                return node_

        return None

    tree = ast.parse(src)
    node = getMethod1(tree)
    result = isPropertyMethod(node)
    assert result == expected

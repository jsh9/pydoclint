import ast
from typing import Optional

import pytest

from pydoclint.utils.special_methods import (
    checkMethodContainsSpecifiedDecorator,
)

src1 = """
class A:
    def method1(self):
        pass
"""

src2 = """
class A:
    @property
    def method1(self):
        pass
"""

src3 = """
class A:
    @hello
    @world
    @property
    @morning
    def method1(self):
        pass
"""

src4 = """
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
    'src, decorator, expected',
    [
        (src1, 'something', False),
        (src2, 'property', True),
        (src3, 'property', True),
        (src4, 'hello_world', True),
        (src4, 'property', False),
    ],
)
def testCheckMethodContainsSpecifiedDecorator(
        src: str,
        decorator: str,
        expected: bool,
) -> None:
    def getMethod1(tree_: ast.AST) -> Optional[ast.FunctionDef]:
        for node_ in ast.walk(tree_):
            if isinstance(node_, ast.FunctionDef) and node_.name == 'method1':
                return node_

        return None

    tree = ast.parse(src)
    node = getMethod1(tree)
    result = checkMethodContainsSpecifiedDecorator(node, decorator=decorator)
    assert result == expected

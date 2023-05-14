import ast

import pytest

from pydoclint.utils import returns
from pydoclint.utils.generic import getFunctionId

src1 = """
def func1():
    return 101
"""

src2 = """
def func2():
    print("No return here")
"""

src3 = """
async def func3():
    def func3_child1():
        print(301)
        def func3_child1_grandchild1():
            print(3011)
    return "async 301"
"""

src4 = """
def func4():
    def func4_child1():
        return "nested 401"

    def func4_child2():
        print('402')
        def func4_child2_grandchild1():
            return 4021
"""

src5 = """
def func5():
    if 1 > 2:
        return 501

    if 2 > 6:
        return 506
"""

src6 = """
def func6():
    if 5 > 4:
        while 3 > 2:
            for i in range(10):
                async for j in range(10):
                    with open('file1') as f1:
                        async with open('file2') as f2:
                            return True
"""

src7 = """
class MyClass:
    def __init__(self):
        pass

    def method1(self):
        print('a1')
        def method1_child1(self):
            pass
        return 2

    @classmethod
    def classmethod1(cls):
        pass
        def classmethod1_child1():
            return 'hello'
"""


@pytest.mark.parametrize(
    'src, expected',
    [
        (src1, True),
        (src2, False),
        (src3, True),
        (src4, False),
        (src5, True),
        (src6, True),
    ],
)
def testHasReturnStatements(src: str, expected: bool) -> None:
    tree = ast.parse(src)
    assert len(tree.body) == 1  # sanity check
    assert isinstance(tree.body[0], ast.FunctionDef | ast.AsyncFunctionDef)
    assert returns.hasReturnStatements(tree.body[0]) == expected


def testHasReturnStatements_inClass() -> None:
    tree = ast.parse(src7)
    assert len(tree.body) == 1  # sanity check
    assert isinstance(tree.body[0], ast.ClassDef)
    assert len(tree.body[0].body) == 3

    expected_list = [False, True, False]
    for node, expected in zip(tree.body[0].body, expected_list):
        assert returns.hasReturnStatements(node) == expected


class ReturnVisitor(ast.NodeVisitor):
    """A helper class to check each return statements in nested functions"""

    def __init__(self):
        self.returnStatements: dict[tuple[int, int, str], bool] = {}
        self.returnAnnotations: dict[tuple[int, int, str], bool] = {}

    def visit_FunctionDef(self, node: ast.FunctionDef | ast.AsyncFunctionDef):
        functionId: tuple[int, int, str] = getFunctionId(node)
        self.returnStatements[functionId] = returns.hasReturnStatements(node)
        self.returnAnnotations[functionId] = returns.hasReturnAnnotation(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        # Treat async functions similarly to regular ones
        self.visit_FunctionDef(node)


srcNested = """ # Return annotations and statementss are intentionally opposite
def func4() -> int:
    def func4_child1():
        return "nested 401"

    def func4_child2() -> float:
        print('402')
        def func4_child2_grandchild1():
            return 4021

    def func4_child3() -> list[str]:
        print(1)

    def func4_child4():
        class NestedClass:
            def func4_child4_grandchild1(self):
                return 2

            def func4_child4_grandchild2(self) -> dict[str, tuple[int, float]]:
                print(1)

        return 1
"""


def testHasReturnStatements_nestedFunction() -> None:
    tree = ast.parse(srcNested)
    visitor = ReturnVisitor()
    visitor.visit(tree)
    result = visitor.returnStatements

    expected = {
        (2, 0, 'func4'): False,
        (3, 4, 'func4_child1'): True,
        (6, 4, 'func4_child2'): False,
        (8, 8, 'func4_child2_grandchild1'): True,
        (11, 4, 'func4_child3'): False,
        (14, 4, 'func4_child4'): True,
        (16, 12, 'func4_child4_grandchild1'): True,
        (19, 12, 'func4_child4_grandchild2'): False,
    }

    assert result == expected


@pytest.mark.parametrize(
    'src, expected',
    [
        ('def func1():\n  return 1', False),
        ('def func1() -> int:\n  print(123)', True),
        ('def func1() -> int | float | None:\n  print(123)', True),
    ],
)
def testHasReturnAnnotation(src: str, expected: bool) -> None:
    tree = ast.parse(src)
    assert len(tree.body) == 1  # sanity check
    assert isinstance(tree.body[0], ast.FunctionDef | ast.AsyncFunctionDef)
    assert returns.hasReturnAnnotation(tree.body[0]) == expected


def testHasReturnAnnotations_nestedFunction() -> None:
    tree = ast.parse(srcNested)
    visitor = ReturnVisitor()
    visitor.visit(tree)
    result = visitor.returnAnnotations

    expected = {
        (2, 0, 'func4'): True,
        (3, 4, 'func4_child1'): False,
        (6, 4, 'func4_child2'): True,
        (8, 8, 'func4_child2_grandchild1'): False,
        (11, 4, 'func4_child3'): True,
        (14, 4, 'func4_child4'): False,
        (16, 12, 'func4_child4_grandchild1'): False,
        (19, 12, 'func4_child4_grandchild2'): True,
    }

    assert result == expected

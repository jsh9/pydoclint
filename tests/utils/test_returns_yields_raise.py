import ast
from typing import Dict, List, Tuple

import pytest

from pydoclint.utils.astTypes import FuncOrAsyncFuncDef
from pydoclint.utils.generic import getFunctionId
from pydoclint.utils.return_yield_raise import (
    getRaisedExceptions,
    hasBareReturnStatements,
    hasGeneratorAsReturnAnnotation,
    hasRaiseStatements,
    hasReturnAnnotation,
    hasReturnStatements,
    hasYieldStatements,
)

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


src8 = """
def func8():
    return
"""


src9 = """
def func9():
    # In tested function, so it doesn't
    # count as having a return statement
    def func9_child1():
        return
"""


src10 = """
def func10():
    # When mixed, we still consider it
    # as having a bare return statement
    if 1 > 2:
        return 501

    if 2 > 6:
        return
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
        (src8, True),
        (src9, False),
        (src10, True),
    ],
)
def testHasReturnStatements(src: str, expected: bool) -> None:
    tree = ast.parse(src)
    assert len(tree.body) == 1  # sanity check
    assert isinstance(tree.body[0], (ast.FunctionDef, ast.AsyncFunctionDef))
    assert hasReturnStatements(tree.body[0]) == expected


@pytest.mark.parametrize(
    'src, expected',
    [
        (src1, False),
        (src2, False),
        (src3, False),
        (src4, False),
        (src5, False),
        (src6, False),
        (src8, True),
        (src9, False),
        (src10, True),
    ],
)
def testHasBareReturnStatements(src: str, expected: bool) -> None:
    tree = ast.parse(src)
    assert len(tree.body) == 1  # sanity check
    assert isinstance(tree.body[0], (ast.FunctionDef, ast.AsyncFunctionDef))
    assert hasBareReturnStatements(tree.body[0]) == expected


def testHasReturnStatements_inClass() -> None:
    tree = ast.parse(src7)
    assert len(tree.body) == 1  # sanity check
    assert isinstance(tree.body[0], ast.ClassDef)
    assert len(tree.body[0].body) == 3

    expected_list = [False, True, False]
    for node, expected in zip(tree.body[0].body, expected_list):
        assert hasReturnStatements(node) == expected


class HelperVisitor(ast.NodeVisitor):
    """A helper class to check each return statements in nested functions"""

    def __init__(self):
        self.returnStatements: Dict[Tuple[int, int, str], bool] = {}
        self.yieldStatements: Dict[Tuple[int, int, str], bool] = {}
        self.raiseStatements: Dict[Tuple[int, int, str], bool] = {}
        self.raisedExceptions: Dict[Tuple[int, int, str], List[str]] = {}
        self.returnAnnotations: Dict[Tuple[int, int, str], bool] = {}
        self.generatorAnnotations: Dict[Tuple[int, int, str], bool] = {}

    def visit_FunctionDef(self, node: FuncOrAsyncFuncDef):
        functionId: Tuple[int, int, str] = getFunctionId(node)
        self.returnStatements[functionId] = hasReturnStatements(node)
        self.yieldStatements[functionId] = hasYieldStatements(node)
        self.raiseStatements[functionId] = hasRaiseStatements(node)
        self.raisedExceptions[functionId] = getRaisedExceptions(node)
        self.returnAnnotations[functionId] = hasReturnAnnotation(node)
        self.generatorAnnotations[functionId] = hasGeneratorAsReturnAnnotation(
            node,
        )
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        # Treat async functions similarly to regular ones
        self.visit_FunctionDef(node)


srcNested = """ # Return annotations and statements are intentionally opposite
def func4() -> int:
    def func4_child1():
        return "nested 401"

    def func4_child2() -> float:
        print('402')
        def func4_child2_grandchild1():
            return 4021

    def func4_child3() -> List[str]:
        print(1)

    def func4_child4():
        class NestedClass:
            def func4_child4_grandchild1(self):
                return 2

            def func4_child4_grandchild2(self) -> Dict[str, Tuple[int, float]]:
                print(1)

        return 1
"""


def testHasReturnStatements_nestedFunction() -> None:
    tree = ast.parse(srcNested)
    visitor = HelperVisitor()
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
    assert isinstance(tree.body[0], (ast.FunctionDef, ast.AsyncFunctionDef))
    assert hasReturnAnnotation(tree.body[0]) == expected


def testHasReturnAnnotations_nestedFunction() -> None:
    tree = ast.parse(srcNested)
    visitor = HelperVisitor()
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


srcGenerator = """
def genFuncExample1() -> Generator[int, None, int]:
    yield 1
    yield 2
    return 3

def genFuncExample2():
    yield 1
    yield 2
    return 3

def someFunc1() -> Generator[int, None, int]:
    return 1

def someFunc2():
    yield from genFuncExample2()

def someFunc3() -> Generator[int, None, None]:
    def someFunc3_child1():
        yield 2

    return 1

def someFunc4():
    yield from range(10)
    def someFunc4_child1():
        yield 2

    yield 3

def someFunc5(arg1):
    if arg1 > 3:
        yield 1

    if arg < -1:
        yield 2
"""


def testHasGeneratorAsReturnAnnotation() -> None:
    tree = ast.parse(srcGenerator)
    visitor = HelperVisitor()
    visitor.visit(tree)
    result = visitor.generatorAnnotations

    expected = {
        (2, 0, 'genFuncExample1'): True,
        (7, 0, 'genFuncExample2'): False,
        (12, 0, 'someFunc1'): True,
        (15, 0, 'someFunc2'): False,
        (18, 0, 'someFunc3'): True,
        (24, 0, 'someFunc4'): False,
        (19, 4, 'someFunc3_child1'): False,
        (26, 4, 'someFunc4_child1'): False,
        (31, 0, 'someFunc5'): False,
    }

    assert result == expected


def testHasYieldStatement() -> None:
    tree = ast.parse(srcGenerator)
    visitor = HelperVisitor()
    visitor.visit(tree)
    result = visitor.yieldStatements

    expected = {
        (2, 0, 'genFuncExample1'): True,
        (7, 0, 'genFuncExample2'): True,
        (12, 0, 'someFunc1'): False,
        (15, 0, 'someFunc2'): True,
        (18, 0, 'someFunc3'): False,
        (24, 0, 'someFunc4'): True,
        (19, 4, 'someFunc3_child1'): True,
        (26, 4, 'someFunc4_child1'): True,
        (31, 0, 'someFunc5'): True,
    }

    assert result == expected


srcRaises = """
def func1(arg1) -> None:
    a = 1
    b = 2
    raise ValueError('Hello world')

def func2():
    raise Exception

def func3(arg1):
    if arg1 > 2:
        raise TypeError

class CustomError(Exception):
    pass

def func4():
    raise CustomError('CustomError')

def func5():
    def func5_child1():
        raise ValueError

    return 1

def func6(arg1):
    if arg1 is None:
        raise TypeError

    return arg1 + 2

def func7(arg0):
    if True:
        raise TypeError

    try:
        "foo"[-10]
    except IndexError as e:
        raise

    try:
        1 / 0
    except ZeroDivisionError:
        raise RuntimeError("a different error")

    try:
        pass
    except OSError as e:
        if e.args[0] == 2 and e.filename:
            fp = None
        else:
            raise

def func8(d):
    try:
        d[0][0]
    except (KeyError, TypeError, m.ValueError):
        raise
    finally:
        pass

def func9(d):
    try:
        d[0]
    except IndexError:
        try:
            d[0][0]
        except KeyError:
            raise AssertionError() from e
        except Exception:
            pass
        if True:
            raise

def func10():
    # no variable resolution is done. this func looks like it throws GError.
    GError = ZeroDivisionError
    try:
        1 / 0
    except GError:
        raise

def func11(a):
    # Duplicated exceptions will only be reported once
    if a < 1:
        raise ValueError

    if a < 2:
        raise ValueError

    if a < 3:
        raise ValueError

    if a < 4:
        raise ValueError

    if a < 5:
        raise ValueError

def func12(a):
    # Exceptions will be reported in alphabetical order, regardless of
    # the order they are raised within the function body

    Error1 = RuntimeError
    Error2 = ValueError
    Error3 = TypeError

    if a < 1:
        raise Error2

    if a < 2:
        raise Error1

    if a < 3:
        raise Error3

def func13(a):
    # ensure we get `Exception`, `Exception()`, and `Exception('something')`
    if a < 1:
        raise ValueError
    elif a < 2:
        raise TypeError()
    else:
        raise IOError('IO Error!')

def func14(a):
    # check that we properly identify submodule exceptions.
    if a < 1:
        raise m.ValueError
    elif a < 2:
        raise m.n.ValueError()
    else:
        raise a.b.c.ValueError(msg="some msg")

def func15():
    try:
        x = 1
    except other.Exception:
        raise

def func16():
    # ensure that "as e" doesn't mess up getting the name of an exception.
    try:
        3 + 3
    except IOError as e:
        raise e
    except (KeyError, IndexError) as e:
        raise e

def func17():
    if a < 1:
        raise MyException.a.b.c(('a', 'b'))
    elif a < 2:
        raise YourException.a.b.c(1)
    elif a < 3:
        raise a.b.c.TheirException.from_str.d.e('my_str')
    elif a < 4:
        raise a.b.c.d.e.f.g.WhoseException.h.i.j.k
    else:
        pass
"""


def testHasRaiseStatements() -> None:
    tree = ast.parse(srcRaises)
    visitor = HelperVisitor()
    visitor.visit(tree)
    result = visitor.raiseStatements

    expected = {
        (2, 0, 'func1'): True,
        (7, 0, 'func2'): True,
        (10, 0, 'func3'): True,
        (17, 0, 'func4'): True,
        (20, 0, 'func5'): False,
        (26, 0, 'func6'): True,
        (21, 4, 'func5_child1'): True,
        (32, 0, 'func7'): True,
        (54, 0, 'func8'): True,
        (62, 0, 'func9'): True,
        (75, 0, 'func10'): True,
        (83, 0, 'func11'): True,
        (100, 0, 'func12'): True,
        (117, 0, 'func13'): True,
        (126, 0, 'func14'): True,
        (135, 0, 'func15'): True,
        (141, 0, 'func16'): True,
        (150, 0, 'func17'): True,
    }

    assert result == expected


def testWhichRaiseStatements() -> None:
    tree = ast.parse(srcRaises)
    visitor = HelperVisitor()
    visitor.visit(tree)
    result = visitor.raisedExceptions

    expected = {
        (2, 0, 'func1'): ['ValueError'],
        (7, 0, 'func2'): ['Exception'],
        (10, 0, 'func3'): ['TypeError'],
        (17, 0, 'func4'): ['CustomError'],
        (20, 0, 'func5'): [],
        (26, 0, 'func6'): ['TypeError'],
        (21, 4, 'func5_child1'): ['ValueError'],
        (32, 0, 'func7'): [
            'IndexError',
            'OSError',
            'RuntimeError',
            'TypeError',
        ],
        (54, 0, 'func8'): ['KeyError', 'TypeError', 'm.ValueError'],
        (62, 0, 'func9'): ['AssertionError', 'IndexError'],
        (75, 0, 'func10'): ['GError'],
        (83, 0, 'func11'): ['ValueError'],
        (100, 0, 'func12'): ['Error1', 'Error2', 'Error3'],
        (117, 0, 'func13'): ['IOError', 'TypeError', 'ValueError'],
        (126, 0, 'func14'): [
            'a.b.c.ValueError',
            'm.ValueError',
            'm.n.ValueError',
        ],
        (135, 0, 'func15'): ['other.Exception'],
        (141, 0, 'func16'): ['IOError', 'IndexError', 'KeyError'],
        (150, 0, 'func17'): [
            # We are unable to detect and drop the parts after "Exception"
            # here, so we will perform partial string matching later.
            'MyException.a.b.c',
            'YourException.a.b.c',
            'a.b.c.TheirException.from_str.d.e',
            'a.b.c.d.e.f.g.WhoseException.h.i.j.k',
        ],
    }

    assert result == expected

import ast
import sys
from pathlib import Path
from textwrap import dedent
from typing import Any

import pytest

from pydoclint.utils.generic import (
    buildClassAttrToDefaultMapping,
    buildFuncArgToDefaultMapping,
    doList1ItemsStartWithList2Items,
    isLastConstructor,
    isPlaceholderDefault,
    isStubFilename,
    stripBacktickWrapper,
    stripQuotes,
)


@pytest.mark.parametrize(
    ('inputStr', 'expected'),
    [
        (None, None),
        ('something', 'something'),
        ('something else', 'something else'),
        ('"good morning"', 'good morning'),
        ('"yes\' good', 'yes good'),
        ('"""""""""', ''),
        ("''''''''''''''''", ''),
        ('""" """  """', '   '),
        ('List["Something", \'Else\']', 'List[Something, Else]'),
        ('`something`', 'something'),
        ('``something``', 'something'),
        ('`List["Something", \'Else\']`', 'List[Something, Else]'),
        ('``List["Something", \'Else\']``', 'List[Something, Else]'),
        ('`""" """  """`', '   '),
        ('``""" """  """``', '   '),
    ],
)
def testStripQuotes(inputStr: str, expected: str) -> None:
    output = stripQuotes(inputStr)
    assert output == expected


@pytest.mark.parametrize(
    ('list1', 'list2', 'expected'),
    [
        ([], [], True),
        (
            ['abc', 'def', 'ghi'],
            ['abc', 'def', 'ghi'],
            True,
        ),
        (
            ['abc', 'def', 'ghi'],
            ['abc', 'def', 'ghi', 'jkl'],
            False,
        ),
        (
            ['abc123', 'def456', 'ghi789'],
            ['abc', 'def', 'ghi'],
            True,
        ),
        (
            ['abc', 'def', 'ghi'],
            ['abc123', 'def456', 'ghi789'],
            False,
        ),
    ],
)
def testDoList1ItemsStartWithList2Items(
        list1: list[str],
        list2: list[str],
        expected: bool,
) -> None:
    output = doList1ItemsStartWithList2Items(list1, list2)
    assert output == expected


@pytest.mark.parametrize(
    ('funcCode', 'expectedMappings'),
    [
        # Case 1: No defaults
        ('def func1(a, b, c): pass', {}),
        # Case 2: Only positional defaults
        ('def func2(a, b=5, c="hello"): pass', {'b': 5, 'c': 'hello'}),
        # Case 3: Mixed positional and keyword-only defaults
        (
            'def func3(a, b=10, *args, c=3.14, d="world"): pass',
            {'b': 10, 'c': 3.14, 'd': 'world'},
        ),
        # Case 4: Complex defaults with various types
        (
            'def fn4(a, b=[1, 2], c=None, *args, d=True, e={"k": "v"}): pass',
            {'b': '[1, 2]', 'c': None, 'd': True, 'e': "{'k': 'v'}"},
        ),
        # Case 5: Complex defaults with type hints and various types
        (
            'def func4(a, *args, d: bool=True, e: str="key"): pass',
            {'d': True, 'e': 'key'},
        ),
        # Case 6: Positional-only and regular arguments share the defaults
        ('def func5(a=1, /, b=2): pass', {'a': 1, 'b': 2}),
        # Case 7: Defaults spanning positional-only, regular, and keyword-only
        (
            'def func6(a, b=2, /, c=3, *, d=4): pass',
            {'b': 2, 'c': 3, 'd': 4},
        ),
        # Case 8: Only positional-only arguments with defaults
        ('def func7(a=1, b=2, /): pass', {'a': 1, 'b': 2}),
        # Case 9: Positional-only argument with a placeholder default (stubs)
        ('def func8(key, default=..., /): pass', {'default': Ellipsis}),
    ],
)
def testBuildFuncArgToDefaultMapping(
        funcCode: str,
        expectedMappings: dict[str, Any],
) -> None:
    tree = ast.parse(funcCode)
    funcDef = tree.body[0]
    mapping = buildFuncArgToDefaultMapping(funcDef)

    # Convert the mapping to a more testable format (arg names to values)
    actualMappings = {}
    for astArg, defaultConstant in mapping.items():
        argName = astArg.arg
        try:
            # Extract the actual value from the AST constant
            defaultValue = defaultConstant.value
        except AttributeError:
            # Handle complex defaults by unparsing them
            defaultValue = ast.unparse(defaultConstant)

        actualMappings[argName] = defaultValue

    assert actualMappings == expectedMappings


@pytest.mark.parametrize(
    ('classCode', 'expectedMappings'),
    [
        # Case 1: No attributes with defaults
        (
            dedent(
                """
                class Test1:
                    pass
                """
            ),
            {},
        ),
        # Case 2: Only typed attributes with defaults
        (
            dedent(
                """
                class Test2:
                    attr1: int = 42
                    attr2: str = "hello"
                """
            ),
            {'attr1': 42, 'attr2': 'hello'},
        ),
        # Case 3: Only untyped attributes
        (
            dedent(
                """
                class Test3:
                    attr1 = 42
                    attr2 = "world"
                """
            ),
            {'attr1': 42, 'attr2': 'world'},
        ),
        # Case 4: Mixed typed and untyped attributes
        (
            dedent(
                """
                class Test4:
                    typed_attr: bool = True
                    untyped_attr = 3.14
                """
            ),
            {'typed_attr': True, 'untyped_attr': 3.14},
        ),
        # Case 5: Complex defaults with various types
        (
            dedent(
                """
                class Test5:
                    set_attr: set = {1, 2, 3, 4, 5, 6}
                    dict_attr = {"key": "value123"}
                    none_attr: str = None
                """
            ),
            {
                'set_attr': '{1, 2, 3, 4, 5, 6}',
                'dict_attr': "{'key': 'value123'}",
                'none_attr': None,
            },
        ),
        # Case 6: Typed attribute without default (should not be included)
        (
            dedent(
                """
                class Test6:
                    attr1: int
                    attr2: str = "hello"
                """
            ),
            {'attr2': 'hello'},
        ),
    ],
)
def testBuildClassAttrToDefaultMapping(
        classCode: str,
        expectedMappings: dict[str, Any],
) -> None:
    tree = ast.parse(classCode)
    classDef = tree.body[0]
    mapping = buildClassAttrToDefaultMapping(classDef)

    # Convert the mapping to a more testable format (attr names to values)
    actualMappings = {}
    for attrName, defaultConstant in mapping.items():
        try:
            # Extract the actual value from the AST constant
            defaultValue = defaultConstant.value
        except AttributeError:
            # Handle complex defaults by unparsing them
            defaultValue = ast.unparse(defaultConstant)

        actualMappings[attrName] = defaultValue

    assert actualMappings == expectedMappings


@pytest.mark.parametrize(
    ('classCode', 'constructorIndex', 'expected'),
    [
        (
            dedent(
                """
                class Sample:
                    def __init__(self):
                        pass
                """
            ),
            0,
            True,
        ),
        (
            dedent(
                """
                class WithOverloads:
                    def __init__(self):
                        pass

                    def helper(self):
                        pass

                    def __init__(self, value):
                        pass
                """
            ),
            0,
            False,
        ),
        (
            dedent(
                """
                class WithOverloads:
                    def __init__(self):
                        pass

                    def helper(self):
                        pass

                    def __init__(self, value):
                        pass
                """
            ),
            1,
            True,
        ),
    ],
)
def testIsLastConstructor(
        classCode: str,
        constructorIndex: int,
        expected: bool,
) -> None:
    tree = ast.parse(classCode)
    classDef = tree.body[0]
    constructors = [
        node
        for node in classDef.body
        if isinstance(node, ast.FunctionDef) and node.name == '__init__'
    ]
    targetConstructor = constructors[constructorIndex]
    output = isLastConstructor(node=targetConstructor, parentClass=classDef)
    assert output == expected


@pytest.mark.parametrize(
    ('filename', 'expected'),
    [
        ('a.pyi', True),
        ('pkg/a.pyi', True),
        (Path('pkg/a.pyi'), True),
        ('a.py', False),
        ('a.pyi.bak', False),
        # Folder scans also find a file named just ".pyi"
        ('.pyi', True),
        # Like folder scans, this follows the platform's case rules
        ('API.PYI', sys.platform == 'win32'),
        ('pkg/x.Pyi', sys.platform == 'win32'),
    ],
)
def testIsStubFilename(filename: str | Path, expected: bool) -> None:
    assert isStubFilename(filename) is expected


@pytest.mark.parametrize(
    ('string', 'expected'),
    [
        ('``int``', 'int'),
        ('`int`', 'int'),
        ('``int, default=3``', 'int, default=3'),
        ("``Literal['a', 'b']``", "Literal['a', 'b']"),
        ('int', 'int'),
        ('``int``, default=3', '``int``, default=3'),  # not wrapping it all
        ('', ''),
    ],
)
def testStripBacktickWrapper(string: str, expected: str) -> None:
    assert stripBacktickWrapper(string) == expected


@pytest.mark.parametrize(
    ('expression', 'expected'),
    [
        ('...', True),
        ('(...)', True),
        ('Ellipsis', False),
        ('None', False),
        ('0', False),
        ("'...'", False),
        ('[...]', False),
    ],
)
def testIsPlaceholderDefault(expression: str, expected: bool) -> None:
    """Test that only the literal ``...`` counts as a placeholder default."""
    node = ast.parse(expression, mode='eval').body
    assert isPlaceholderDefault(node) is expected

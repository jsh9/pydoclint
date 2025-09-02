import ast

import pytest

from pydoclint.utils.generic import (
    buildClassAttrToDefaultMapping,
    buildFuncArgToDefaultMapping,
    doList1ItemsStartWithList2Items,
    stripQuotes,
)


@pytest.mark.parametrize(
    'inputStr, expected',
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
    'list1, list2, expected',
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
    'funcCode, expectedMappings',
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
    ],
)
def testBuildFuncArgToDefaultMapping(
        funcCode: str,
        expectedMappings: dict[str, any],
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
    'classCode, expectedMappings',
    [
        # Case 1: No attributes with defaults
        (
            """
class Test1:
    pass
""",
            {},
        ),
        # Case 2: Only typed attributes with defaults
        (
            """
class Test2:
    attr1: int = 42
    attr2: str = "hello"
""",
            {'attr1': 42, 'attr2': 'hello'},
        ),
        # Case 3: Only untyped attributes
        (
            """
class Test3:
    attr1 = 42
    attr2 = "world"
""",
            {'attr1': 42, 'attr2': 'world'},
        ),
        # Case 4: Mixed typed and untyped attributes
        (
            """
class Test4:
    typed_attr: bool = True
    untyped_attr = 3.14
""",
            {'typed_attr': True, 'untyped_attr': 3.14},
        ),
        # Case 5: Complex defaults with various types
        (
            """
class Test5:
    set_attr: set = {1, 2, 3, 4, 5, 6}
    dict_attr = {"key": "value123"}
    none_attr: str = None
""",
            {
                'set_attr': '{1, 2, 3, 4, 5, 6}',
                'dict_attr': "{'key': 'value123'}",
                'none_attr': None,
            },
        ),
        # Case 6: Typed attribute without default (should not be included)
        (
            """
class Test6:
    attr1: int
    attr2: str = "hello"
""",
            {'attr2': 'hello'},
        ),
    ],
)
def testBuildClassAttrToDefaultMapping(
        classCode: str,
        expectedMappings: dict[str, any],
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

import ast

import pytest

from pydoclint.utils.generic import (
    buildArgToDefaultMapping,
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
            'def func4(a, b=[1, 2], c=None, *args, d=True, e={"key": "value"}): pass',
            {'b': [1, 2], 'c': None, 'd': True, 'e': {'key': 'value'}},
        ),
        # Case 5: Complex defaults with type hints and various types
        (
            'def func4(a, *args, d: bool=True, e: str="key"): pass',
            {'d': True, 'e': 'key'},
        ),
    ],
)
def testBuildArgToDefaultMapping(
        funcCode: str,
        expectedMappings: dict[str, any],
) -> None:
    tree = ast.parse(funcCode)
    funcDef = tree.body[0]
    mapping = buildArgToDefaultMapping(funcDef)

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
            # For the test cases, we need to evaluate some expressions
            if defaultValue == '[1, 2]':
                defaultValue = [1, 2]
            elif defaultValue == "{'key': 'value'}":
                defaultValue = {'key': 'value'}

        actualMappings[argName] = defaultValue

    assert actualMappings == expectedMappings

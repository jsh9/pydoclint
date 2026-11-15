import ast
import sys
from pathlib import Path
from textwrap import dedent
from typing import Any

import pytest

from pydoclint.utils.generic import (
    _isPythonExpression,
    _normalizeExpression,
    buildClassAttrToDefaultMapping,
    buildFuncArgToDefaultMapping,
    defaultValuesEqual,
    doList1ItemsStartWithList2Items,
    getDefaultValue,
    isDefaultOnly,
    isLastConstructor,
    isPlaceholderDefault,
    isStubFilename,
    splitOuterDefault,
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
    ('typeHint', 'expected'),
    [
        (', default=3', True),
        (',default = 3', True),
        ('\n  , default=3', True),
        ('``, default=3``', True),
        ('', False),
        ('int', False),
        ('int, default=3', False),
        ("Annotated[int, 'units, default=3']", False),
        # TODO: Recognize other ways of writing a default, and update these
        #  cases. For now, only `, default=` starts a default (see
        #  docs/style_deviations.md). See:
        #  https://github.com/jsh9/pydoclint/issues/336
        (', default is 3', False),
        (', default: 3', False),
        ('default=3', False),  # no comma before `default`
    ],
)
def testIsDefaultOnly(typeHint: str, expected: bool) -> None:
    assert isDefaultOnly(typeHint) is expected


@pytest.mark.parametrize(
    ('typeHint', 'expected'),
    [
        ('int, default=3', ('int', '3')),
        (', default=3', ('', '3')),
        ('int , default = [1, 2]', ('int', '[1, 2]')),
        ('``int, default=3``', ('int', '3')),
        ('int, optional, default=3', ('int, optional', '3')),
        (
            "Annotated[int, 'units, default=3'], default=5",
            ("Annotated[int, 'units, default=3']", '5'),
        ),
        ("str, default=', default=x'", ('str', "', default=x'")),
        ('int', None),
        ("Annotated[int, 'units, default=3']", None),  # only inside the type
        ('list of int, default=3', None),  # not valid Python before it
        # TODO: Recognize other ways of writing a default, and update these
        #  cases. For now, only `, default=` starts a default (see
        #  docs/style_deviations.md). See:
        #  https://github.com/jsh9/pydoclint/issues/336
        ('int, default is 3', None),
        ('int, default: 3', None),
    ],
)
def testSplitOuterDefault(
        typeHint: str,
        expected: tuple[str, str] | None,
) -> None:
    assert splitOuterDefault(typeHint) == expected


@pytest.mark.parametrize(
    ('typeHint', 'expected'),
    [
        ('', None),
        ('int', None),
        ('int, default=3', '3'),
        (', default=3', '3'),
        ('``int, default=3``', '3'),
        ("Annotated[int, 'units, default=3']", None),
        ("Annotated[int, 'units, default=3'], default=5", '5'),
        # Docstring types that aren't valid Python
        ('list of int, default=None', 'None'),
        ('array-like of shape (n,), default=None', 'None'),
        ('``int``, default=3', '3'),
        ('``list of int, default=3``', '3'),  # backticks around it all
        # The default itself contains `, default=`: after a type that isn't
        # valid Python, the default starts at the first `, default=`
        (
            'dict of str to int, default=dict(a=1, default=2)',
            'dict(a=1, default=2)',
        ),
        ("list of str, default=', default=y'", "', default=y'"),
        # TODO: Recognize other ways of writing a default, and update these
        #  cases. For now, only `, default=` starts a default (see
        #  docs/style_deviations.md). See:
        #  https://github.com/jsh9/pydoclint/issues/336
        ('int, default is 3', None),
        ('int, default: 3', None),
        (', default 3', None),
    ],
)
def testGetDefaultValue(typeHint: str, expected: str | None) -> None:
    assert getDefaultValue(typeHint) == expected


@pytest.mark.parametrize(
    ('default1', 'default2', 'expected'),
    [
        (None, None, True),
        ('3', None, False),
        (None, '3', False),
        ('3', '3', True),
        ('3', '4', False),
        ("'a'", '"a"', True),
        ('a', "'a'", False),
        ('0.00001', '1e-05', True),
        ('[1,2]', '[1, 2]', True),
        ('42  # noqa: E501', '42', True),
        ('all rows', 'all  rows', False),  # not valid Python: compare as text
        ('all rows', 'all rows', True),
        ('all rows  # noqa', 'all rows', True),  # comments are ignored
        # A `#` inside quotes is not a comment (unlike in specialEqual(); see
        # https://github.com/jsh9/pydoclint/issues/337)
        ("'#1f77b4'", "'#ff0000'", False),
    ],
)
def testDefaultValuesEqual(
        default1: str | None,
        default2: str | None,
        expected: bool,
) -> None:
    assert defaultValuesEqual(default1, default2) is expected


@pytest.mark.parametrize(
    ('text', 'expected'),
    [
        ('int', True),
        ('  int\n', True),  # surrounding whitespace is ignored
        ('int, optional', True),  # a tuple
        ("Annotated[int, 'units, default=3']", True),
        ('array-like', True),  # a subtraction
        ('', False),
        ('   ', False),
        ('list of int', False),
        ("Annotated[int, 'units", False),  # unclosed string and bracket
        ('`int`', False),
        ('int, default=3', False),
    ],
)
def testIsPythonExpression(text: str, expected: bool) -> None:
    assert _isPythonExpression(text) is expected


@pytest.mark.parametrize(
    ('text', 'expected'),
    [
        ('3', '3'),
        ('  3\n', '3'),
        ('"a"', "'a'"),
        ("'a'", "'a'"),
        ('0.00001', '1e-05'),
        ('[1,2]', '[1, 2]'),
        ('42  # noqa: E501', '42'),  # comments are dropped
        ('int, optional', '(int, optional)'),
        ('', None),
        ('all rows', None),
        ("'unclosed", None),
    ],
)
def testNormalizeExpression(text: str, expected: str | None) -> None:
    assert _normalizeExpression(text) == expected


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

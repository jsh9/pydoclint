import ast
from typing import TYPE_CHECKING

import pytest

from pydoclint.utils.arg import Arg, ArgList
from pydoclint.utils.visitor_helper import (
    addStarsToDocstringArgsWhenApplicable,
    extractClassAttributesFromNode,
    extractReturnTypeFromGenerator,
    extractYieldTypeFromGeneratorOrIteratorAnnotation,
    getDocumentedAndActualClassArgLists,
)

if TYPE_CHECKING:
    from pydoclint.utils.violation import Violation


@pytest.mark.parametrize(
    ('returnAnnoText', 'hasGen', 'hasIter', 'expected'),
    [
        ('Generator', True, False, 'Generator'),
        ('AsyncGenerator', True, False, 'AsyncGenerator'),
        ('Generator[None, None, None]', True, False, 'None'),
        ('Generator[int, None, str]', True, False, 'int'),
        ('AsyncGenerator[int, None, str]', True, False, 'int'),
        ('Generator[bool, None, str]', True, False, 'bool'),
        ('Generator["MyClass", None, str]', True, False, 'MyClass'),
        (
            'Generator[Union[str, int], None, str]',
            True,
            False,
            'Union[str, int]',
        ),
        (
            'Generator[str | int | float | bool | "MyClass", None, str]',
            True,
            False,
            'str | int | float | bool | MyClass',
        ),
        (
            'Generator[Literal["a", "b", "c"], None, str]',
            True,
            False,
            "Literal['a', 'b', 'c']",
        ),
        (
            'Generator[\n    Literal["a",\n"b",\n\t\n\n"c"], None, str]',
            True,
            False,
            "Literal['a', 'b', 'c']",
        ),
        ('Iterator', False, True, 'Iterator'),
        ('AsyncIterator', False, True, 'AsyncIterator'),
        ('Iterable', False, True, 'Iterable'),
        ('AsyncIterable', False, True, 'AsyncIterable'),
        ('Iterator[None]', False, True, 'None'),
        ('Iterator[int]', False, True, 'int'),
        ('AsyncIterator[int]', False, True, 'int'),
        ('Iterable[int]', False, True, 'int'),
        ('AsyncIterable[int]', False, True, 'int'),
        ('Iterator[bool]', False, True, 'bool'),
        ('Iterator["MyClass"]', False, True, 'MyClass'),
        (
            'Iterator[Union[str, int]]',
            False,
            True,
            'Union[str, int]',
        ),
        (
            'Iterator[str | int | float | bool | "MyClass"]',
            False,
            True,
            'str | int | float | bool | MyClass',
        ),
        (
            'Iterator[Literal["a", "b", "c"]]',
            False,
            True,
            "Literal['a', 'b', 'c']",
        ),
        (
            'Iterator[\n    Literal["a",\n"b",\n\t\n\n"c"]]',
            False,
            True,
            "Literal['a', 'b', 'c']",
        ),
    ],
)
def testExtractYieldTypeFromGeneratorOrIteratorAnnotation(
        returnAnnoText: str,
        hasGen: bool,
        hasIter: bool,
        expected: str,
) -> None:
    extracted = extractYieldTypeFromGeneratorOrIteratorAnnotation(
        returnAnnoText=returnAnnoText,
        hasGeneratorAsReturnAnnotation=hasGen,
        hasIteratorOrIterableAsReturnAnnotation=hasIter,
    )
    assert extracted == expected


@pytest.mark.parametrize(
    ('returnAnnoText', 'expected'),
    [
        ('Generator[int, None, str]', 'str'),
        ('AsyncGenerator[int, None, str]', 'str'),
        ('Generator[bool, None, float]', 'float'),
        ('Generator[None, None, "MyClass"]', 'MyClass'),
        (
            'Generator[None, str, Union[str, int]]',
            'Union[str, int]',
        ),
        (
            'Generator[str, None, str | int | float | bool | "MyClass"]',
            'str | int | float | bool | MyClass',
        ),
        (
            'Generator[None, str, Literal["a", "b", "c"]]',
            "Literal['a', 'b', 'c']",
        ),
        (
            'Generator[None, str, \n    Literal["a",\n"b",\n\t\n\n"c"]]',
            "Literal['a', 'b', 'c']",
        ),
    ],
)
def testExtractReturnTypeFromGenerator(
        returnAnnoText: str,
        expected: str,
) -> None:
    extracted = extractReturnTypeFromGenerator(returnAnnoText)
    assert extracted == expected


@pytest.mark.parametrize(
    ('funcArgs', 'docArgs', 'expected'),
    [
        # No args anywhere, so we expect the helper to return an empty ArgList
        # unchanged.
        pytest.param(
            ArgList([]),
            ArgList([]),
            ArgList([]),
            id='both-lists-empty',
        ),
        # Signature has *args but docstring omits it, so there is nothing to
        # convert and we still expect [].
        pytest.param(
            ArgList([Arg(name='*args', typeHint='')]),
            ArgList([]),
            ArgList([]),
            id='signature-has-star-docstring-omits-it',
        ),
        # Docstring documents a non-star arg not present in signature, so we
        # expect it to remain as-is.
        pytest.param(
            ArgList([]),
            ArgList([Arg(name='args', typeHint='int')]),
            ArgList([Arg(name='args', typeHint='int')]),
            id='docstring-only-entries-non-starred',
        ),
        # Docstring already uses **args while signature only has *args, so
        # `expected` keeps the doc entries untouched.
        pytest.param(
            ArgList([Arg(name='*args', typeHint='int')]),
            ArgList([Arg(name='**args', typeHint='int')]),
            ArgList([Arg(name='**args', typeHint='int')]),
            id='docstring-uses-more-stars-than-signature-int',
        ),
        # Same mismatched stars as above but with tuple hints; `expected` again
        # preserves the doc entries.
        pytest.param(
            ArgList([Arg(name='*args', typeHint='tuple[int, ...]')]),
            ArgList([Arg(name='**args', typeHint='tuple[int, ...]')]),
            ArgList([Arg(name='**args', typeHint='tuple[int, ...]')]),
            id='docstring-uses-more-stars-than-signature-tuple',
        ),
        # Docstring has args/kwargs without leading stars, so `expected` shows
        # them rewritten to *args/**kwargs.
        pytest.param(
            ArgList([
                Arg(name='*args', typeHint='Tuple[int, ...]'),
                Arg(name='**kwargs', typeHint='dict[str, str]'),
                Arg(name='param', typeHint='float'),
            ]),
            ArgList([
                Arg(name='args', typeHint='Tuple[int, ...]'),
                Arg(name='kwargs', typeHint='dict[str, str]'),
                Arg(name='param', typeHint='float'),
            ]),
            ArgList([
                Arg(name='*args', typeHint='Tuple[int, ...]'),
                Arg(name='**kwargs', typeHint='dict[str, str]'),
                Arg(name='param', typeHint='float'),
            ]),
            id='docstring-missing-stars-for-both-args-and-kwargs',
        ),
        # Normal positional parameters do not involve varargs, so `expected`
        # mirrors the doc inputs exactly.
        pytest.param(
            ArgList([
                Arg(name='param', typeHint='int'),
                Arg(name='param2', typeHint='str'),
            ]),
            ArgList([
                Arg(name='param', typeHint='int'),
                Arg(name='param2', typeHint='str'),
            ]),
            ArgList([
                Arg(name='param', typeHint='int'),
                Arg(name='param2', typeHint='str'),
            ]),
            id='no-varargs-anywhere',
        ),
        # Docstring already uses the correct starred names, so `expected` stays
        # identical.
        pytest.param(
            ArgList([
                Arg(name='*args', typeHint=''),
                Arg(name='**kwargs', typeHint=''),
            ]),
            ArgList([
                Arg(name='*args', typeHint='Any'),
                Arg(name='**kwargs', typeHint='Any'),
            ]),
            ArgList([
                Arg(name='*args', typeHint='Any'),
                Arg(name='**kwargs', typeHint='Any'),
            ]),
            id='docstring-already-has-correct-stars',
        ),
        # Signature itself has oddly prefixed kwargs, and we expect the helper
        # to leave doc entries unchanged.
        pytest.param(
            ArgList([
                Arg(name='*args', typeHint=''),
                Arg(name='***********kwargs', typeHint=''),
            ]),
            ArgList([
                Arg(name='*args', typeHint='Any'),
                Arg(name='**kwargs', typeHint='Any'),
            ]),
            ArgList([
                Arg(name='*args', typeHint='Any'),
                Arg(name='**kwargs', typeHint='Any'),
            ]),
            id='signature-varargs-already-overstarred',
        ),
        # Signature has extra stars while docstring provides non-starred names,
        # so `expected` mirrors signature (overstarred), even if this is odd.
        pytest.param(
            ArgList([
                Arg(name='*****args', typeHint=''),
                Arg(name='***********kwargs', typeHint=''),
            ]),
            ArgList([
                Arg(name='args', typeHint='Any'),
                Arg(name='kwargs', typeHint='Any'),
            ]),
            ArgList([
                Arg(name='*****args', typeHint='Any'),
                Arg(name='***********kwargs', typeHint='Any'),
            ]),
            id='docstring-missing-stars-but-signature-overstarred',
        ),
    ],
)
def testAddStarsToDocstringArgsWhenApplicable(
        funcArgs: ArgList,
        docArgs: ArgList,
        expected: ArgList,
) -> None:
    normalized = addStarsToDocstringArgsWhenApplicable(
        docArgs=docArgs,
        funcArgs=funcArgs,
    )

    assert normalized.infoList == expected.infoList


@pytest.mark.parametrize(
    ('docPriv', 'treatProp', 'expected'),
    [
        (
            True,
            True,
            ArgList([
                Arg(name='a1', typeHint=''),
                Arg(name='attr1', typeHint='int'),
                Arg(name='attr2', typeHint='float'),
                Arg(name='attr3', typeHint=''),
                Arg(name='attr4', typeHint=''),
                Arg(name='attr5', typeHint=''),
                Arg(name='attr6', typeHint=''),
                Arg(name='attr7', typeHint=''),
                Arg(name='attr8', typeHint=''),
                Arg(name='attr9', typeHint=''),
                Arg(name='attr10', typeHint=''),
                Arg(name='attr11', typeHint=''),
                Arg(name='attr12', typeHint='bool'),
                Arg(name='a13', typeHint=''),
                Arg(name='a14', typeHint=''),
                Arg(name='a15', typeHint=''),
                Arg(name='a16', typeHint=''),
                Arg(name='a17', typeHint=''),
                Arg(name='a18', typeHint=''),
                Arg(name='a19', typeHint=''),
                Arg(name='a20', typeHint=''),
                Arg(name='a21', typeHint=''),
                Arg(name='_privAttr1', typeHint='int'),
                Arg(name='prop1', typeHint='float | str | dict | None'),
                Arg(name='_privProp', typeHint='str'),
            ]),
        ),
        (
            False,
            False,
            ArgList([
                Arg(name='a1', typeHint=''),
                Arg(name='attr1', typeHint='int'),
                Arg(name='attr2', typeHint='float'),
                Arg(name='attr3', typeHint=''),
                Arg(name='attr4', typeHint=''),
                Arg(name='attr5', typeHint=''),
                Arg(name='attr6', typeHint=''),
                Arg(name='attr7', typeHint=''),
                Arg(name='attr8', typeHint=''),
                Arg(name='attr9', typeHint=''),
                Arg(name='attr10', typeHint=''),
                Arg(name='attr11', typeHint=''),
                Arg(name='attr12', typeHint='bool'),
                Arg(name='a13', typeHint=''),
                Arg(name='a14', typeHint=''),
                Arg(name='a15', typeHint=''),
                Arg(name='a16', typeHint=''),
                Arg(name='a17', typeHint=''),
                Arg(name='a18', typeHint=''),
                Arg(name='a19', typeHint=''),
                Arg(name='a20', typeHint=''),
                Arg(name='a21', typeHint=''),
            ]),
        ),
        (
            True,
            False,
            ArgList([
                Arg(name='a1', typeHint=''),
                Arg(name='attr1', typeHint='int'),
                Arg(name='attr2', typeHint='float'),
                Arg(name='attr3', typeHint=''),
                Arg(name='attr4', typeHint=''),
                Arg(name='attr5', typeHint=''),
                Arg(name='attr6', typeHint=''),
                Arg(name='attr7', typeHint=''),
                Arg(name='attr8', typeHint=''),
                Arg(name='attr9', typeHint=''),
                Arg(name='attr10', typeHint=''),
                Arg(name='attr11', typeHint=''),
                Arg(name='attr12', typeHint='bool'),
                Arg(name='a13', typeHint=''),
                Arg(name='a14', typeHint=''),
                Arg(name='a15', typeHint=''),
                Arg(name='a16', typeHint=''),
                Arg(name='a17', typeHint=''),
                Arg(name='a18', typeHint=''),
                Arg(name='a19', typeHint=''),
                Arg(name='a20', typeHint=''),
                Arg(name='a21', typeHint=''),
                Arg(name='_privAttr1', typeHint='int'),
            ]),
        ),
        (
            False,
            True,
            ArgList([
                Arg(name='a1', typeHint=''),
                Arg(name='attr1', typeHint='int'),
                Arg(name='attr2', typeHint='float'),
                Arg(name='attr3', typeHint=''),
                Arg(name='attr4', typeHint=''),
                Arg(name='attr5', typeHint=''),
                Arg(name='attr6', typeHint=''),
                Arg(name='attr7', typeHint=''),
                Arg(name='attr8', typeHint=''),
                Arg(name='attr9', typeHint=''),
                Arg(name='attr10', typeHint=''),
                Arg(name='attr11', typeHint=''),
                Arg(name='attr12', typeHint='bool'),
                Arg(name='a13', typeHint=''),
                Arg(name='a14', typeHint=''),
                Arg(name='a15', typeHint=''),
                Arg(name='a16', typeHint=''),
                Arg(name='a17', typeHint=''),
                Arg(name='a18', typeHint=''),
                Arg(name='a19', typeHint=''),
                Arg(name='a20', typeHint=''),
                Arg(name='a21', typeHint=''),
                Arg(name='prop1', typeHint='float | str | dict | None'),
            ]),
        ),
    ],
)
def testExtractClassAttributesFromNode(
        docPriv: bool,
        treatProp: bool,
        expected: ArgList,
) -> None:
    code: str = """
class MyClass:
    a1 = 1
    attr1: int = 1
    attr2: float = 1.0
    attr3, attr4, attr5 = 1, 2, 3
    attr6 = attr7 = attr8 = attr9 = attr10 = -1
    attr11 = attr1 == 2
    attr12: bool = attr1 == 2
    a13, a14, a15 = a16, a17, a18 = a19, a20, a21 = (1, 2), 3, 4
    _privAttr1: int = 12345

    @property
    def prop1(self) -> float | str | dict | None:
        return 2.2

    @property
    def _privProp(self) -> str:
        return 'secret'

    def nonProperty(self) -> int:
        return 1
"""
    parsed = ast.parse(code)
    extracted: ArgList = extractClassAttributesFromNode(
        node=parsed.body[0],
        shouldDocumentPrivateClassAttributes=docPriv,
        treatPropertyMethodsAsClassAttrs=treatProp,
        onlyAttrsWithClassVarAreTreatedAsClassAttrs=False,
        checkArgDefaults=False,
    )
    assert extracted == expected


@pytest.mark.parametrize(
    ('onlyAttrsWithClassVarAreTreatedAsClassAttrs', 'expected'),
    [
        (
            True,
            ArgList([
                Arg(name='a', typeHint='int'),
                Arg(name='c', typeHint='str'),
            ]),
        ),
        (
            False,
            ArgList([
                Arg(name='a', typeHint='ClassVar[int]'),
                Arg(name='b', typeHint='bool'),
                Arg(name='c', typeHint='ClassVar[str]'),
                Arg(name='d', typeHint='float'),
            ]),
        ),
    ],
)
def testExtractClassAttributesFromNode_ClassVarOnly(
        onlyAttrsWithClassVarAreTreatedAsClassAttrs: bool,
        expected: ArgList,
) -> None:
    code: str = """
from typing import ClassVar

class MyClass:
    a: ClassVar[int]
    b: bool
    c: ClassVar[str]
    d: float = 1.0
"""
    parsed = ast.parse(code)
    extracted: ArgList = extractClassAttributesFromNode(
        node=parsed.body[1],
        shouldDocumentPrivateClassAttributes=False,
        treatPropertyMethodsAsClassAttrs=False,
        onlyAttrsWithClassVarAreTreatedAsClassAttrs=(
            onlyAttrsWithClassVarAreTreatedAsClassAttrs
        ),
        checkArgDefaults=False,
    )
    assert extracted == expected


src1 = '''
class SimpleInlineDoc:
    """A class for testing and experimenting with code snippets."""

    field1 = 5
    """Inline documentation for classvar."""
'''

src2 = '''
class InlineDocAfter:
    """Another class for testing."""

    field1: int = 10
    """Inline documentation for classvar."""

    field2: str
    """Inline documentation for an instance variable."""

    field3: int = 5
    """Inline documentation for another classvar."""
'''

src3 = '''
class MixedAttributeDoc:
    """
    A class with mixed attribute documentation styles.

    {attribute_documentation}Documentation for field2 using the attribute directive.
    """

    field1: int = 42
    """Documentation for field1 placed after the declaration."""

    field2: str = "str"
'''


@pytest.mark.parametrize(
    ('src', 'style', 'attribute_documentation'),
    [
        (src1, 'sphinx', None),
        (src1, 'google', None),
        (src1, 'numpy', None),
        (src2, 'sphinx', None),
        (src2, 'google', None),
        (src2, 'numpy', None),
        (
            src3,
            'sphinx',
            '.. attribute :: field2\n   \n:type: str\n',
        ),
        (
            src3,
            'google',
            'Attributes:\n\tfield2 (str): ',
        ),
        (
            src3,
            'numpy',
            # the Parameters section is required in numpy style for attribute docs
            # even if it is empty
            'Parameters\n----------\n\nAttributes\n----------\nfield2 : str\n\t',
        ),
    ],
)
def testAllowInlineClassvarDocs(
        src: str,
        style: str,
        attribute_documentation: str | None,
) -> None:
    final_src = src.format(
        attribute_documentation=attribute_documentation or ''
    )
    parsed = ast.parse(final_src)
    node = parsed.body[0]
    assert isinstance(node, ast.ClassDef)

    violations: list[Violation] = []
    attrs = getDocumentedAndActualClassArgLists(
        node=node,
        style=style,
        shouldDocumentPrivateClassAttributes=False,
        treatPropertyMethodsAsClassAttributes=False,
        onlyAttrsWithClassVarAreTreatedAsClassAttrs=False,
        checkArgDefaults=False,
        violations=violations,
        skipCheckingShortDocstrings=False,
        allowInlineClassVarDocs=True,
    )
    assert attrs is not None
    assert not violations
    documentedAttrs, actualAttrs = attrs
    assert documentedAttrs == actualAttrs

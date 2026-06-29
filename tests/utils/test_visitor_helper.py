import ast
from typing import TYPE_CHECKING

import pytest

from pydoclint.utils.arg import Arg, ArgList
from pydoclint.utils.return_anno import ReturnAnnotation
from pydoclint.utils.return_yield_raise import GeneratorAnnotationKind
from pydoclint.utils.unparser_custom import unparseName
from pydoclint.utils.visitor_helper import (
    _extractAnnotationSubscriptArgs,
    _extractAnnotationSubscriptSlice,
    _extractAsyncGeneratorAnnotationSubscriptArgs,
    _extractGeneratorAnnotationSubscriptArgs,
    _extractGeneratorOrAsyncGeneratorAnnotationArgs,
    addStarsToDocstringArgsWhenApplicable,
    extractClassAttributesFromNode,
    extractReturnTypeFromGeneratorAnnotation,
    extractYieldTypeFromGeneratorOrIteratorAnnotation,
    getDocumentedAndActualClassArgLists,
    getReturnTypeToDocument,
    updateDocumentedArgListWithInlineDocstrings,
)

if TYPE_CHECKING:
    from pydoclint.utils.violation import Violation


@pytest.mark.parametrize(
    ('returnAnnoText', 'generatorAnnotationKind', 'hasIter', 'expected'),
    [
        ('Generator', GeneratorAnnotationKind.GENERATOR, False, 'Generator'),
        (
            'AsyncGenerator',
            GeneratorAnnotationKind.ASYNC_GENERATOR,
            False,
            'AsyncGenerator',
        ),
        ('Generator[None]', GeneratorAnnotationKind.GENERATOR, False, 'None'),
        ('Generator[int]', GeneratorAnnotationKind.GENERATOR, False, 'int'),
        (
            'Generator[int, str]',
            GeneratorAnnotationKind.GENERATOR,
            False,
            'int',
        ),
        (
            'Generator[int, str, bool]',
            GeneratorAnnotationKind.GENERATOR,
            False,
            'int',
        ),
        (
            'AsyncGenerator[int]',
            GeneratorAnnotationKind.ASYNC_GENERATOR,
            False,
            'int',
        ),
        (
            'AsyncGenerator[int, str]',
            GeneratorAnnotationKind.ASYNC_GENERATOR,
            False,
            'int',
        ),
        (  # 4 Generator args are malformed; keep full annotation.
            'Generator[int, str, bool, bytes]',
            GeneratorAnnotationKind.GENERATOR,
            False,
            'Generator[int, str, bool, bytes]',
        ),
        (  # 3 AsyncGenerator args are malformed; keep full annotation.
            'AsyncGenerator[int, str, bool]',
            GeneratorAnnotationKind.ASYNC_GENERATOR,
            False,
            'AsyncGenerator[int, str, bool]',
        ),
        (  # 4 AsyncGenerator args are malformed; keep full annotation.
            'AsyncGenerator[int, str, bool, bytes]',
            GeneratorAnnotationKind.ASYNC_GENERATOR,
            False,
            'AsyncGenerator[int, str, bool, bytes]',
        ),
        (
            'Generator[None, None, None]',
            GeneratorAnnotationKind.GENERATOR,
            False,
            'None',
        ),
        (
            'Generator[int, None, str]',
            GeneratorAnnotationKind.GENERATOR,
            False,
            'int',
        ),
        (
            'AsyncGenerator[int, None, str]',
            GeneratorAnnotationKind.ASYNC_GENERATOR,
            False,
            'AsyncGenerator[int, None, str]',
        ),
        (
            'Generator[bool, None, str]',
            GeneratorAnnotationKind.GENERATOR,
            False,
            'bool',
        ),
        (
            'Generator["MyClass", None, str]',
            GeneratorAnnotationKind.GENERATOR,
            False,
            'MyClass',
        ),
        (
            'Generator[Dict[str, int]]',
            GeneratorAnnotationKind.GENERATOR,
            False,
            'Dict[str, int]',
        ),
        (
            'Generator[Union[str, int], None, str]',
            GeneratorAnnotationKind.GENERATOR,
            False,
            'Union[str, int]',
        ),
        (
            'Generator[str | int | float | bool | "MyClass", None, str]',
            GeneratorAnnotationKind.GENERATOR,
            False,
            'str | int | float | bool | MyClass',
        ),
        (
            'Generator[Literal["a", "b", "c"], None, str]',
            GeneratorAnnotationKind.GENERATOR,
            False,
            "Literal['a', 'b', 'c']",
        ),
        (
            'Generator[\n    Literal["a",\n"b",\n\t\n\n"c"], None, str]',
            GeneratorAnnotationKind.GENERATOR,
            False,
            "Literal['a', 'b', 'c']",
        ),
        ('Iterator', None, True, 'Iterator'),
        ('AsyncIterator', None, True, 'AsyncIterator'),
        ('Iterable', None, True, 'Iterable'),
        ('AsyncIterable', None, True, 'AsyncIterable'),
        ('Iterator[None]', None, True, 'None'),
        ('Iterator[int]', None, True, 'int'),
        ('AsyncIterator[int]', None, True, 'int'),
        ('Iterable[int]', None, True, 'int'),
        ('AsyncIterable[int]', None, True, 'int'),
        ('Iterator[int, str]', None, True, '(int, str)'),
        ('Iterable[int, str]', None, True, '(int, str)'),
        ('AsyncIterator[int, str]', None, True, '(int, str)'),
        ('AsyncIterable[int, str]', None, True, '(int, str)'),
        ('Iterator[bool]', None, True, 'bool'),
        ('Iterator["MyClass"]', None, True, 'MyClass'),
        (
            'Iterator[Union[str, int]]',
            None,
            True,
            'Union[str, int]',
        ),
        (
            'Iterator[str | int | float | bool | "MyClass"]',
            None,
            True,
            'str | int | float | bool | MyClass',
        ),
        (
            'Iterator[Literal["a", "b", "c"]]',
            None,
            True,
            "Literal['a', 'b', 'c']",
        ),
        (
            'Iterator[\n    Literal["a",\n"b",\n\t\n\n"c"]]',
            None,
            True,
            "Literal['a', 'b', 'c']",
        ),
    ],
)
def testExtractYieldTypeFromGeneratorOrIteratorAnnotation(
        returnAnnoText: str,
        generatorAnnotationKind: GeneratorAnnotationKind | None,
        hasIter: bool,
        expected: str,
) -> None:
    """
    Verify yield extraction for Generator, Iterator, and Iterable.

    The abbreviated Generator cases guard against DOC404 regressions where the
    whole annotation is compared with the docstring yield type. AsyncGenerator
    cases pass the kind flag explicitly because the production visitor owns
    annotation-kind detection.
    """
    extracted = extractYieldTypeFromGeneratorOrIteratorAnnotation(
        returnAnnoText=returnAnnoText,
        generatorAnnotationKind=generatorAnnotationKind,
        hasIteratorOrIterableAsReturnAnnotation=hasIter,
    )
    assert extracted == expected


@pytest.mark.parametrize(
    ('returnAnnoText', 'generatorAnnotationKind', 'expected'),
    [
        ('Generator', GeneratorAnnotationKind.GENERATOR, 'Generator'),
        ('Generator[int]', GeneratorAnnotationKind.GENERATOR, 'None'),
        ('Generator[int, str]', GeneratorAnnotationKind.GENERATOR, 'None'),
        (
            'Generator[int, str, bool]',
            GeneratorAnnotationKind.GENERATOR,
            'bool',
        ),
        (
            'AsyncGenerator[int]',
            GeneratorAnnotationKind.ASYNC_GENERATOR,
            'None',
        ),
        (
            'AsyncGenerator[int, str]',
            GeneratorAnnotationKind.ASYNC_GENERATOR,
            'None',
        ),
        (  # 4 Generator args are malformed; keep full annotation.
            'Generator[int, str, bool, bytes]',
            GeneratorAnnotationKind.GENERATOR,
            'Generator[int, str, bool, bytes]',
        ),
        (  # 3 AsyncGenerator args are malformed; keep full annotation.
            'AsyncGenerator[int, str, bool]',
            GeneratorAnnotationKind.ASYNC_GENERATOR,
            'AsyncGenerator[int, str, bool]',
        ),
        (  # 4 AsyncGenerator args are malformed; keep full annotation.
            'AsyncGenerator[int, str, bool, bytes]',
            GeneratorAnnotationKind.ASYNC_GENERATOR,
            'AsyncGenerator[int, str, bool, bytes]',
        ),
        (
            'Generator[Dict[str, int]]',
            GeneratorAnnotationKind.GENERATOR,
            'None',
        ),
        (
            'Generator[int, None, str]',
            GeneratorAnnotationKind.GENERATOR,
            'str',
        ),
        (
            'AsyncGenerator[int, None, str]',
            GeneratorAnnotationKind.ASYNC_GENERATOR,
            'AsyncGenerator[int, None, str]',
        ),
        (
            'Generator[bool, None, float]',
            GeneratorAnnotationKind.GENERATOR,
            'float',
        ),
        (
            'Generator[None, None, "MyClass"]',
            GeneratorAnnotationKind.GENERATOR,
            'MyClass',
        ),
        (
            'Generator[None, str, Union[str, int]]',
            GeneratorAnnotationKind.GENERATOR,
            'Union[str, int]',
        ),
        (
            'Generator[str, None, str | int | float | bool | "MyClass"]',
            GeneratorAnnotationKind.GENERATOR,
            'str | int | float | bool | MyClass',
        ),
        (
            'Generator[None, str, Literal["a", "b", "c"]]',
            GeneratorAnnotationKind.GENERATOR,
            "Literal['a', 'b', 'c']",
        ),
        (
            'Generator[None, str, \n    Literal["a",\n"b",\n\t\n\n"c"]]',
            GeneratorAnnotationKind.GENERATOR,
            "Literal['a', 'b', 'c']",
        ),
    ],
)
def testExtractReturnTypeFromGeneratorAnnotation(
        returnAnnoText: str,
        generatorAnnotationKind: GeneratorAnnotationKind,
        expected: str,
) -> None:
    """
    Verify Generator return extraction, including PEP 696 defaults.

    The two-argument case is necessary because its second arg is SendType, not
    ReturnType, so pydoclint must compare returns against the default None.
    AsyncGenerator cases pass the kind flag explicitly so return extraction
    does not infer annotation kind from raw strings.
    """
    extracted = extractReturnTypeFromGeneratorAnnotation(
        returnAnnoText,
        generatorAnnotationKind=generatorAnnotationKind,
    )
    assert extracted == expected


@pytest.mark.parametrize(
    ('returnAnnoText', 'generatorAnnotationKind', 'expected'),
    [
        ('Iterator[int]', None, 'Iterator[int]'),
        ('Generator[int]', GeneratorAnnotationKind.GENERATOR, 'None'),
        ('Generator[int, str]', GeneratorAnnotationKind.GENERATOR, 'None'),
        (
            'Generator[int, str, bool]',
            GeneratorAnnotationKind.GENERATOR,
            'bool',
        ),
        (
            'AsyncGenerator[int, str]',
            GeneratorAnnotationKind.ASYNC_GENERATOR,
            'None',
        ),
        (
            'Generator[int, str, bool, bytes]',
            GeneratorAnnotationKind.GENERATOR,
            'Generator[int, str, bool, bytes]',
        ),
    ],
)
def testGetReturnTypeToDocument(
        returnAnnoText: str,
        generatorAnnotationKind: GeneratorAnnotationKind | None,
        expected: str,
) -> None:
    """Verify return-documentation type selection stays centralized."""
    extracted = getReturnTypeToDocument(
        returnAnnotation=ReturnAnnotation(returnAnnoText),
        generatorAnnotationKind=generatorAnnotationKind,
    )
    assert extracted == expected


@pytest.mark.parametrize(
    ('returnAnnoText', 'generatorAnnotationKind', 'expected'),
    [
        ('Generator[int]', GeneratorAnnotationKind.GENERATOR, ['int']),
        (
            'Generator[int, str]',
            GeneratorAnnotationKind.GENERATOR,
            ['int', 'str'],
        ),
        (
            'Generator[int, str, bool]',
            GeneratorAnnotationKind.GENERATOR,
            ['int', 'str', 'bool'],
        ),
        (
            'AsyncGenerator[int]',
            GeneratorAnnotationKind.ASYNC_GENERATOR,
            ['int'],
        ),
        (
            'AsyncGenerator[int, str]',
            GeneratorAnnotationKind.ASYNC_GENERATOR,
            ['int', 'str'],
        ),
    ],
)
def testExtractGeneratorOrAsyncGeneratorAnnotationArgs(
        returnAnnoText: str,
        generatorAnnotationKind: GeneratorAnnotationKind,
        expected: list[str],
) -> None:
    """Verify generator-like annotation args use the supplied kind's arity."""
    extracted = _extractGeneratorOrAsyncGeneratorAnnotationArgs(
        returnAnnoText,
        generatorAnnotationKind=generatorAnnotationKind,
    )
    assert [unparseName(arg) for arg in extracted] == expected


@pytest.mark.parametrize(
    ('returnAnnoText', 'generatorAnnotationKind', 'expectedError'),
    [
        (
            'Generator[int, str, bool, bytes]',
            GeneratorAnnotationKind.GENERATOR,
            ValueError,
        ),
        (
            'AsyncGenerator[int, str, bool]',
            GeneratorAnnotationKind.ASYNC_GENERATOR,
            ValueError,
        ),
        (
            'AsyncGenerator[int, str, bool, bytes]',
            GeneratorAnnotationKind.ASYNC_GENERATOR,
            ValueError,
        ),
        ('Generator', GeneratorAnnotationKind.GENERATOR, AttributeError),
        (
            'AsyncGenerator',
            GeneratorAnnotationKind.ASYNC_GENERATOR,
            AttributeError,
        ),
    ],
)
def testExtractGeneratorOrAsyncGeneratorAnnotationArgsRaises(
        returnAnnoText: str,
        generatorAnnotationKind: GeneratorAnnotationKind,
        expectedError: type[Exception],
) -> None:
    """Verify generator-like arg extraction preserves invalid-shape errors."""
    with pytest.raises(expectedError):
        _extractGeneratorOrAsyncGeneratorAnnotationArgs(
            returnAnnoText,
            generatorAnnotationKind=generatorAnnotationKind,
        )


@pytest.mark.parametrize(
    ('returnAnnoText', 'expected'),
    [
        ('Generator[int]', ['int']),
        ('Generator[int, str]', ['int', 'str']),
        ('Generator[int, str, bool]', ['int', 'str', 'bool']),
        ('Generator[Dict[str, int]]', ['Dict[str, int]']),
    ],
)
def testExtractGeneratorAnnotationSubscriptArgs(
        returnAnnoText: str,
        expected: list[str],
) -> None:
    """Verify valid Generator arities are extracted as AST args."""
    extracted = _extractGeneratorAnnotationSubscriptArgs(returnAnnoText)
    assert [unparseName(arg) for arg in extracted] == expected


@pytest.mark.parametrize(
    ('returnAnnoText', 'expectedError'),
    [
        ('Generator[int, str, bool, bytes]', ValueError),
        ('Generator', AttributeError),
    ],
)
def testExtractGeneratorAnnotationSubscriptArgsRaises(
        returnAnnoText: str,
        expectedError: type[Exception],
) -> None:
    """Verify Generator arg extraction rejects unsupported shapes."""
    with pytest.raises(expectedError):
        _extractGeneratorAnnotationSubscriptArgs(returnAnnoText)


@pytest.mark.parametrize(
    ('returnAnnoText', 'expected'),
    [
        ('AsyncGenerator[int]', ['int']),
        ('AsyncGenerator[int, str]', ['int', 'str']),
        ('AsyncGenerator[Dict[str, int]]', ['Dict[str, int]']),
    ],
)
def testExtractAsyncGeneratorAnnotationSubscriptArgs(
        returnAnnoText: str,
        expected: list[str],
) -> None:
    """Verify valid AsyncGenerator arities are extracted as AST args."""
    extracted = _extractAsyncGeneratorAnnotationSubscriptArgs(returnAnnoText)
    assert [unparseName(arg) for arg in extracted] == expected


@pytest.mark.parametrize(
    ('returnAnnoText', 'expectedError'),
    [
        ('AsyncGenerator[int, str, bool]', ValueError),
        ('AsyncGenerator[int, str, bool, bytes]', ValueError),
        ('AsyncGenerator', AttributeError),
    ],
)
def testExtractAsyncGeneratorAnnotationSubscriptArgsRaises(
        returnAnnoText: str,
        expectedError: type[Exception],
) -> None:
    """Verify AsyncGenerator arg extraction rejects unsupported shapes."""
    with pytest.raises(expectedError):
        _extractAsyncGeneratorAnnotationSubscriptArgs(returnAnnoText)


@pytest.mark.parametrize(
    ('returnAnnoText', 'expected'),
    [
        ('Generator[int]', ['int']),
        ('Generator[int, str]', ['int', 'str']),
        ('Generator[Dict[str, int]]', ['Dict[str, int]']),
    ],
)
def testExtractAnnotationSubscriptArgs(
        returnAnnoText: str,
        expected: list[str],
) -> None:
    """Verify generic subscript args keep single, tuple, and nested forms."""
    extracted = _extractAnnotationSubscriptArgs(returnAnnoText)
    assert [unparseName(arg) for arg in extracted] == expected


@pytest.mark.parametrize(
    ('returnAnnoText', 'expectedError'),
    [
        ('Generator', AttributeError),
        (None, TypeError),
    ],
)
def testExtractAnnotationSubscriptArgsRaises(
        returnAnnoText: str | None,
        expectedError: type[Exception],
) -> None:
    """Verify generic subscript arg extraction preserves parser errors."""
    with pytest.raises(expectedError):
        _extractAnnotationSubscriptArgs(returnAnnoText)


@pytest.mark.parametrize(
    ('returnAnnoText', 'expected'),
    [
        ('Generator[int]', 'int'),
        ('Generator[int, str]', '(int, str)'),
        ('Generator[Dict[str, int]]', 'Dict[str, int]'),
    ],
)
def testExtractAnnotationSubscriptSlice(
        returnAnnoText: str,
        expected: str,
) -> None:
    """Verify generic subscript slice extraction returns the raw AST slice."""
    extracted = _extractAnnotationSubscriptSlice(returnAnnoText)
    assert unparseName(extracted) == expected


@pytest.mark.parametrize(
    ('returnAnnoText', 'expectedError'),
    [
        ('Generator', AttributeError),
        (None, TypeError),
    ],
)
def testExtractAnnotationSubscriptSliceRaises(
        returnAnnoText: str | None,
        expectedError: type[Exception],
) -> None:
    """Verify generic subscript slice extraction preserves parser errors."""
    with pytest.raises(expectedError):
        _extractAnnotationSubscriptSlice(returnAnnoText)


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
    """int: Inline documentation for classvar."""

    field2: str
    """str: Inline documentation for an instance variable."""

    field3: int = 5
    """int: Inline documentation for another classvar."""
'''

src3 = '''
class MixedAttributeDoc:
    """
    A class with mixed attribute documentation styles.

    {attribute_documentation}Documentation for field2 using the attribute directive.
    """

    field1: int = 42
    """int: Documentation for field1 placed after the declaration."""

    field2: str = "str"
'''

sphinx_attr_doc = '.. attribute :: field2\n   \n:type: str\n'
google_attr_doc = 'Attributes:\n\tfield2 (str): '
# the Parameters section is required in numpy style for attribute docs
# even if it is empty
numpy_attr_doc = (
    'Parameters\n----------\n\nAttributes\n----------\nfield2 : str\n\t'
)


@pytest.mark.parametrize(
    ('src', 'style', 'attribute_documentation', 'expected_violations'),
    [
        (src1, 'sphinx', None, []),
        (src1, 'google', None, []),
        (src1, 'numpy', None, []),
        (src2, 'sphinx', None, []),
        (src2, 'google', None, []),
        (src2, 'numpy', None, []),
        (
            src3,
            'sphinx',
            sphinx_attr_doc,
            [607],
        ),
        (
            src3,
            'google',
            google_attr_doc,
            [607],
        ),
        (
            src3,
            'numpy',
            numpy_attr_doc,
            [607],
        ),
    ],
)
@pytest.mark.parametrize('argTypeHintsInDocstring', [True, False])
def testRequireInlineClassvarDocs(
        src: str,
        style: str,
        attribute_documentation: str | None,
        argTypeHintsInDocstring: bool,
        expected_violations: list[int],
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
        requireInlineClassVarDocs=True,
        argTypeHintsInDocstring=argTypeHintsInDocstring,
    )
    assert attrs is not None
    assert [v.code for v in violations] == expected_violations


expected_src1 = [Arg(name='field1', typeHint='')]
expected_src2 = [
    Arg(name='field1', typeHint='int'),
    Arg(name='field2', typeHint='str'),
    Arg(name='field3', typeHint='int'),
]
expected_doc_src3 = [Arg(name='field1', typeHint='int')]
expected_actual_src3 = [
    Arg(name='field1', typeHint='int'),
    Arg(name='field2', typeHint='str'),
]

src4 = '''
class DocstringMismatch:
    """A class where some of the inline docstrings are missing."""

    field1: int = 42

    field2: str = "str"
    """Documentation for field2"""
'''

src5 = '''
class DocstringTypeMismatch:
    """A class where the inline docstring types do not match the annotation."""

    field1: int = 42
    """str: This field is actually a string, not an int."""
'''

src4_expected_doc = [Arg(name='field2', typeHint='')]
src4_expected_actual = [
    Arg(name='field1', typeHint='int'),
    Arg(name='field2', typeHint='str'),
]
src5_expected_doc = [Arg(name='field1', typeHint='str')]
src5_expected_actual = [Arg(name='field1', typeHint='int')]


@pytest.mark.parametrize(
    (
        'src',
        'style',
        'attribute_documentation',
        'expected_docargs',
        'expected_actualargs',
        'expected_violations',
    ),
    [
        (
            src1,
            'sphinx',
            None,
            expected_src1,
            expected_src1,
            [],
        ),
        (
            src1,
            'google',
            None,
            expected_src1,
            expected_src1,
            [],
        ),
        (
            src1,
            'numpy',
            None,
            expected_src1,
            expected_src1,
            [],
        ),
        (src2, 'sphinx', None, expected_src2, expected_src2, []),
        (src2, 'google', None, expected_src2, expected_src2, []),
        (src2, 'numpy', None, expected_src2, expected_src2, []),
        (
            src3,
            'sphinx',
            sphinx_attr_doc,
            expected_doc_src3,
            expected_actual_src3,
            # expect DOC607 because inline docs are required in this mode
            [607],
        ),
        (
            src3,
            'google',
            google_attr_doc,
            expected_doc_src3,
            expected_actual_src3,
            [607],
        ),
        (
            src3,
            'numpy',
            numpy_attr_doc,
            expected_doc_src3,
            expected_actual_src3,
            [607],
        ),
        (
            src4,
            'sphinx',
            None,
            src4_expected_doc,
            src4_expected_actual,
            [],
        ),
        (
            src4,
            'google',
            None,
            src4_expected_doc,
            src4_expected_actual,
            [],
        ),
        (
            src4,
            'numpy',
            None,
            src4_expected_doc,
            src4_expected_actual,
            [],
        ),
        (
            src5,
            'sphinx',
            None,
            src5_expected_doc,
            src5_expected_actual,
            # a violation is not thrown at this level for mismatched types
            [],
        ),
        (
            src5,
            'google',
            None,
            src5_expected_doc,
            src5_expected_actual,
            # a violation is not thrown at this level for mismatched types
            [],
        ),
        (
            src5,
            'numpy',
            None,
            src5_expected_doc,
            src5_expected_actual,
            # a violation is not thrown at this level for mismatched types
            [],
        ),
    ],
)
def testGetDocumentedAndActualClassArgListsWithInlineClassVarDocs(
        src: str,
        style: str,
        attribute_documentation: str | None,
        expected_docargs: list[Arg],
        expected_actualargs: list[Arg],
        expected_violations: list[int],
) -> None:
    final_src = src.format(
        attribute_documentation=attribute_documentation or ''
    )
    parsed = ast.parse(final_src)
    node = parsed.body[0]
    assert isinstance(node, ast.ClassDef)

    violations: list[Violation] = []
    docArgs, actualArgs = getDocumentedAndActualClassArgLists(
        node=node,
        style=style,
        shouldDocumentPrivateClassAttributes=False,
        treatPropertyMethodsAsClassAttributes=False,
        onlyAttrsWithClassVarAreTreatedAsClassAttrs=False,
        checkArgDefaults=False,
        violations=violations,
        skipCheckingShortDocstrings=False,
        requireInlineClassVarDocs=True,
        argTypeHintsInDocstring=True,
    ) or (None, None)

    assert [v.code for v in violations] == expected_violations
    assert docArgs == ArgList(expected_docargs)
    assert actualArgs == ArgList(expected_actualargs)


expected_doc_src3_no_inline = [Arg(name='field2', typeHint='str')]
expected_actual_src3_no_inline = [
    Arg(name='field1', typeHint='int'),
    Arg(name='field2', typeHint='str'),
]


@pytest.mark.parametrize(
    (
        'src',
        'style',
        'attribute_documentation',
        'expected_docargs',
        'expected_actualargs',
        'expected_violations',
    ),
    [
        (
            src3,
            'sphinx',
            sphinx_attr_doc,
            expected_doc_src3_no_inline,
            expected_actual_src3_no_inline,
            # Expect DOC606 because inline docstrings are not accepted here
            [606],
        ),
        (
            src3,
            'google',
            google_attr_doc,
            expected_doc_src3_no_inline,
            expected_actual_src3_no_inline,
            # Expect DOC606 because inline docstrings are not accepted here
            [606],
        ),
        (
            src3,
            'numpy',
            numpy_attr_doc,
            expected_doc_src3_no_inline,
            expected_actual_src3_no_inline,
            # Expect DOC606 because inline docstrings are not accepted here
            [606],
        ),
    ],
)
def testGetDocumentedAndActualClassArgListsWithoutInlinveClassVarDocs(
        src: str,
        style: str,
        attribute_documentation: str | None,
        expected_docargs: list[Arg],
        expected_actualargs: list[Arg],
        expected_violations: list[int],
) -> None:
    final_src = src.format(
        attribute_documentation=attribute_documentation or ''
    )
    parsed = ast.parse(final_src)
    node = parsed.body[0]
    assert isinstance(node, ast.ClassDef)

    violations: list[Violation] = []
    docArgs, actualArgs = getDocumentedAndActualClassArgLists(
        node=node,
        style=style,
        shouldDocumentPrivateClassAttributes=False,
        treatPropertyMethodsAsClassAttributes=False,
        onlyAttrsWithClassVarAreTreatedAsClassAttrs=False,
        checkArgDefaults=False,
        violations=violations,
        skipCheckingShortDocstrings=False,
        requireInlineClassVarDocs=False,
        argTypeHintsInDocstring=True,
    ) or (None, None)

    assert [v.code for v in violations] == expected_violations
    assert docArgs == ArgList(expected_docargs)
    assert actualArgs == ArgList(expected_actualargs)


@pytest.mark.parametrize(
    (
        'src',
        'initial_docArgs',
        'requireInlineClassVarDocs',
        'shouldDocumentPrivateClassAttributes',
        'argTypeHintsInDocstring',
        'expected_docargs',
        'expected_violations',
    ),
    [
        # src1: Simple inline doc without type hints
        (
            src1,
            ArgList([]),
            True,
            False,
            True,
            [Arg(name='field1', typeHint='')],
            [],
        ),
        (
            src1,
            ArgList([]),
            True,
            False,
            False,
            [Arg(name='field1', typeHint='')],
            [],
        ),
        (
            src1,
            ArgList([]),
            False,
            False,
            True,
            [],
            [606],
        ),
        # src2: Multiple inline docs with type hints
        (
            src2,
            ArgList([]),
            True,
            False,
            True,
            [
                Arg(name='field1', typeHint='int'),
                Arg(name='field2', typeHint='str'),
                Arg(name='field3', typeHint='int'),
            ],
            [],
        ),
        (
            src2,
            ArgList([]),
            True,
            False,
            False,
            [
                Arg(name='field1', typeHint=''),
                Arg(name='field2', typeHint=''),
                Arg(name='field3', typeHint=''),
            ],
            [],
        ),
        (
            src2,
            ArgList([]),
            False,
            False,
            True,
            [],
            [606, 606, 606],
        ),
        # src4: Partial inline docs (field1 has no doc, field2 has doc)
        (
            src4,
            ArgList([]),
            True,
            False,
            True,
            [Arg(name='field2', typeHint='')],
            [],
        ),
        (
            src4,
            ArgList([]),
            False,
            False,
            True,
            [],
            [606],
        ),
        # src5: Type mismatch between annotation and inline doc
        (
            src5,
            ArgList([]),
            True,
            False,
            True,
            [Arg(name='field1', typeHint='str')],
            [],
        ),
        (
            src5,
            ArgList([]),
            True,
            False,
            False,
            [Arg(name='field1', typeHint='')],
            [],
        ),
    ],
)
def testUpdateDocumentedArgListWithInlineDocstrings(
        src: str,
        initial_docArgs: ArgList,
        requireInlineClassVarDocs: bool,
        shouldDocumentPrivateClassAttributes: bool,
        argTypeHintsInDocstring: bool,
        expected_docargs: list[Arg],
        expected_violations: list[int],
) -> None:
    parsed = ast.parse(src)
    node = parsed.body[0]
    assert isinstance(node, ast.ClassDef)

    # Extract actual args from the class
    actualArgs = extractClassAttributesFromNode(
        node=node,
        shouldDocumentPrivateClassAttributes=shouldDocumentPrivateClassAttributes,
        treatPropertyMethodsAsClassAttrs=False,
        onlyAttrsWithClassVarAreTreatedAsClassAttrs=False,
        checkArgDefaults=False,
    )

    # Start with initial docArgs
    docArgs = ArgList(list(initial_docArgs.infoList))
    violations: list[Violation] = []

    # Call the function to test
    updateDocumentedArgListWithInlineDocstrings(
        node=node,
        docArgs=docArgs,
        actualArgs=actualArgs,
        shouldDocumentPrivateClassAttributes=shouldDocumentPrivateClassAttributes,
        argTypeHintsInDocstring=argTypeHintsInDocstring,
        requireInlineClassVarDocs=requireInlineClassVarDocs,
        violations=violations,
    )

    # Verify results
    assert [v.code for v in violations] == expected_violations
    assert docArgs == ArgList(expected_docargs)

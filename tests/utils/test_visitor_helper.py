import pytest

from pydoclint.utils.visitor_helper import (
    extractReturnTypeFromGenerator,
    extractYieldTypeFromGeneratorOrIteratorAnnotation,
)


@pytest.mark.parametrize(
    'returnAnnoText, hasGen, hasIter, expected',
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
    'returnAnnoText, expected',
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

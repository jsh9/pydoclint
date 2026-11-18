import pytest

from pydoclint.utils.return_anno import ReturnAnnotation


@pytest.mark.parametrize(
    ('annotation', 'expected'),
    [
        (None, False),
        ('', False),
        ('    ', False),
        ('Tuple[int]', True),
        ('Tuple[int, str]', True),
        ('Tuple[int, str, bool]', True),
        ('Tuple[int, str, None, Dict[str, Any]]', True),
        ('Tuple[int, ...]', True),
        ('tuple[int, str]', True),
        ('Optional[Tuple[int, str]]', False),
        ('Union[Tuple[int, str], Tuple[int, str]]', False),
        ('tuple[int, str] | tuple[int, bool]', False),
        ('tuple[str, str, bool, bool] | None', False),
        ('tuple[int | str, str | bool, bool | float]', True),
        ('int', False),
        ('(int, str, bool)', False),
        ('tuple(int, str, bool)', False),
        ('Tuple(int, str, bool)', False),
        ('tuple(1, 2, 3)', False),
        ("'tuple[int, int, str]'", True),
        ('"tuple[int, int, str]"', True),
        ("'tuple'[int, int, str]", True),
        ('Annotated[int, "#x"]', False),
        ("Literal['a]', 'b']", False),
        ('tuple[Annotated[int, "#x"], str]', True),
        ("Tuple[Literal['a]', 'b'], int]", True),
        ('tuple[]', False),
        ('int |', False),
    ],
)
def testIsTuple(annotation: str | None, expected: bool) -> None:
    retAnno = ReturnAnnotation(annotation=annotation)
    assert retAnno._isTuple() == expected


@pytest.mark.parametrize(
    ('annotation', 'expected'),
    [
        (None, []),
        ('int', ['int']),
        ('Tuple[int]', ['int']),
        ('Tuple[int, str]', ['int', 'str']),
        ('Tuple[int, ...]', ['Tuple[int, ...]']),
        ('tuple[()]', []),
        ('tuple[list[int]]', ['list[int]']),
        ('Tuple["MyClass", int]', ['MyClass', 'int']),
        ('Annotated[int, "#x"]', ['Annotated[int, #x]']),
        ("Literal['a]', 'b']", ["Literal['a], b]"]),
        (
            "tuple[Annotated[int, \"#x\"], Literal['a]', 'b']]",
            ['Annotated[int, #x]', "Literal['a], b]"],
        ),
    ],
)
def testDecompose(annotation: str | None, expected: list[str]) -> None:
    retAnno = ReturnAnnotation(annotation=annotation)
    assert retAnno.decompose() == expected

import pytest

from pydoclint.utils.return_anno import ReturnAnnotation


@pytest.mark.parametrize(
    'annotation, expected',
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
    ],
)
def testIsTuple(annotation: str, expected: bool) -> None:
    retAnno = ReturnAnnotation(annotation=annotation)
    assert retAnno._isTuple() == expected

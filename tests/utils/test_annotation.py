import ast
from typing import Optional

import pytest

from pydoclint.utils.annotation import parseAnnotation


def testParseAnnotationInArguments() -> None:
    src = """
def foo(
        arg1: Optional[Union[int, float]],
        arg2: Tuple[str, int, float],
        arg3: Dict[str, Any],
        arg4: Set[int],
        arg5: List[float],
        arg6: int | float | None,
        arg7: Any,
        arg8: SomeType[List[Dict[str, Any]], SomeOtherType],
        arg9: None,
        arg10,
        arg11,
):
    pass
"""
    tree = ast.parse(src)

    result = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            result = _getArgTypeHints(node)

    expected: dict[str, str] = {
        'arg1': 'Optional[Union[int, float]]',
        'arg2': 'Tuple[str, int, float]',
        'arg3': 'Dict[str, Any]',
        'arg4': 'Set[int]',
        'arg5': 'List[float]',
        'arg6': 'int | float | None',
        'arg7': 'Any',
        'arg8': 'SomeType[List[Dict[str, Any]], SomeOtherType]',
        'arg9': 'None',
        'arg10': None,
        'arg11': None,
    }

    assert result == expected


def _getArgTypeHints(node: ast.FunctionDef) -> dict[str, str]:
    hints = {}
    for arg_ in node.args.args:
        hints[arg_.arg] = parseAnnotation(arg_.annotation)

    return hints


@pytest.mark.parametrize(
    'src, expectedAnnotation',
    [
        ('def func():\n    pass', None),
        ('def func(arg1, arg2):\n    pass', None),
        ('def func() -> int:\n    pass', 'int'),
        ('def func() -> list[int]:\n    pass', 'list[int]'),
        ('def func() -> List[int]:\n    pass', 'List[int]'),
        ('def func() -> Optional[int]:\n    pass', 'Optional[int]'),
        ('def func() -> Dict[str, Any]:\n    pass', 'Dict[str, Any]'),
        ('def func() -> CustomType:\n    pass', 'CustomType'),
        (
            'def func() -> int | dict[str, Any] | None | list[int]:\n    pass',
            'int | dict[str, Any] | None | list[int]',
        ),
    ],
)
def testParseReturnAnnotation(src: str, expectedAnnotation: str):
    tree = ast.parse(src)

    returnAnnotation: Optional[str] = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            returnAnnotation: str = parseAnnotation(node.returns)

    assert returnAnnotation == expectedAnnotation

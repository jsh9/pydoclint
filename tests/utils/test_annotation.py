import ast
import sys
from typing import Dict, Optional

import pytest

from pydoclint.utils.unparser_custom import unparseName


def testUnparseAnnotationInArguments() -> None:
    src = """
def foo(
        arg01: Optional[Union[int, float]],
        arg02: Tuple[str, int, float],
        arg03: Dict[str, Any],
        arg04: Set[int],
        arg05: List[float],
        arg06: int | float | None,
        arg07: Any,
        arg08: SomeType[List[Dict[str, Any]], SomeOtherType],
        arg09: None,
        arg10,
        arg11: List[ast.arg],
        arg12: Dict[str, Tuple[ast.arg, np.ndarray]],
        arg13: Tuple[str, ...],
        arg14: Tuple[None, int, float, None],
        arg15: Callable[[T], U],
        arg16: Callable[[int, str, bool], float],
        arg17: Callable[..., ReturnType],
        arg18: Callable[ParamSpecVariable, ReturnType],
        arg19: Callable[Concatenate[Arg1Type, Arg2Type, ..., ParamSpecVariable], ReturnType],  # noqa: LN002
        arg20: Type[User],
        arg21: Type[BasicUser | ProUser],
        arg22: Literal[True],
        arg23: ClassVar[dict[str, int]],
        arg24: TypeGuard[list[str]],
        arg25: TypeVarTuple('Ts'),
        arg26: Annotated[int, ValueRange(-10, 5)],
        arg27: Annotated[int, ValueRange(3, 10), ctype('char')],
        arg28: 'MyClass',
        arg29: TypeVar('A', str, bytes),
        arg30: TypeVar('U', bound=str | bytes),
):
    pass
"""
    tree = ast.parse(src)

    result = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            result = _getArgTypeHints(node)

    expected: Dict[str, str] = {
        'arg01': 'Optional[Union[int, float]]',
        'arg02': 'Tuple[str, int, float]',
        'arg03': 'Dict[str, Any]',
        'arg04': 'Set[int]',
        'arg05': 'List[float]',
        'arg06': 'int | float | None',
        'arg07': 'Any',
        'arg08': 'SomeType[List[Dict[str, Any]], SomeOtherType]',
        'arg09': 'None',
        'arg10': None,
        'arg11': 'List[ast.arg]',
        'arg12': 'Dict[str, Tuple[ast.arg, np.ndarray]]',
        'arg13': 'Tuple[str, ...]',
        'arg14': 'Tuple[None, int, float, None]',
        'arg15': 'Callable[[T], U]',
        'arg16': 'Callable[[int, str, bool], float]',
        'arg17': 'Callable[..., ReturnType]',
        'arg18': 'Callable[ParamSpecVariable, ReturnType]',
        'arg19': 'Callable[Concatenate[Arg1Type, Arg2Type, ..., ParamSpecVariable], ReturnType]',
        'arg20': 'Type[User]',
        'arg21': 'Type[BasicUser | ProUser]',
        'arg22': 'Literal[True]',
        'arg23': 'ClassVar[dict[str, int]]',
        'arg24': 'TypeGuard[list[str]]',
        'arg25': "TypeVarTuple('Ts')",
        'arg26': 'Annotated[int, ValueRange(-10, 5)]',
        'arg27': "Annotated[int, ValueRange(3, 10), ctype('char')]",
        'arg28': "'MyClass'",
        'arg29': "TypeVar('A', str, bytes)",
        'arg30': "TypeVar('U', bound=str | bytes)",
    }

    assert result == expected


def testUnparseAnnotationInArguments_py311() -> None:
    if sys.version_info < (3, 11):
        assert True
        return  # this test is only runnable in Python 3.11

    src = """
def foo(
        arg01: tuple[T, *Ts],
        arg02: tuple[*Ts, T],
        arg03: Callable[[*Ts], None],
        arg04: tuple[*Shape],
        arg05: Optional[tuple[*Shape]],
):
    pass
"""
    tree = ast.parse(src)

    result = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            result = _getArgTypeHints(node)

    expected: Dict[str, str] = {
        'arg01': 'tuple[T, *Ts]',
        'arg02': 'tuple[*Ts, T]',
        'arg03': 'Callable[[*Ts], None]',
        'arg04': 'tuple[*Shape]',
        'arg05': 'Optional[tuple[*Shape]]',
    }

    assert result == expected


def _getArgTypeHints(node: ast.FunctionDef) -> Dict[str, str]:
    hints = {}
    for arg_ in node.args.args:
        hints[arg_.arg] = unparseName(arg_.annotation)

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
            returnAnnotation: str = unparseName(node.returns)

    assert returnAnnotation == expectedAnnotation

from __future__ import annotations

import ast
from typing import TYPE_CHECKING

import pytest
from click.testing import CliRunner

from pydoclint.main import _checkFile
from pydoclint.main import main as cliMain
from pydoclint.utils.return_yield_raise import getRaisedExceptions

if TYPE_CHECKING:
    from pathlib import Path


def _buildDocstring(style: str, raisedTypes: list[str] | None) -> str:
    if raisedTypes is None:
        return '    """Perform an operation."""\n'

    if style == 'numpy':
        entries = '\n'.join(
            f'    {excType}\n        If an error occurs.'
            for excType in raisedTypes
        )
        return (
            '    """\n'
            '    Perform an operation.\n\n'
            '    Raises\n'
            '    ------\n'
            f'{entries}\n'
            '    """\n'
        )

    if style == 'google':
        entries = '\n'.join(
            f'        {excType}: If an error occurs.'
            for excType in raisedTypes
        )
        return (
            '    """Perform an operation.\n\n'
            '    Raises:\n'
            f'{entries}\n'
            '    """\n'
        )

    entries = '\n'.join(
        f'    :raises {excType}: If an error occurs.'
        for excType in raisedTypes
    )
    return f'    """Perform an operation.\n\n{entries}\n    """\n'


@pytest.mark.parametrize('style', ['numpy', 'google', 'sphinx'])
@pytest.mark.parametrize(
    ('documentedTypes', 'expectedCodes'),
    [
        (['RuntimeError'], []),
        (['ValueError'], ['DOC503']),
        (None, ['DOC501', 'DOC503']),
    ],
)
def testRaisedExceptionVariableWithAddNote(
        tmp_path: Path,
        style: str,
        documentedTypes: list[str] | None,
        expectedCodes: list[str],
) -> None:
    docstring = _buildDocstring(style, documentedTypes)
    source = (
        'def bar() -> None:\n'
        f'{docstring}'
        '    exc = RuntimeError("An error occurred in bar")\n'
        '    exc.add_note("Additional context.")\n'
        '    raise exc\n'
    )
    samplePath = tmp_path / 'sample.py'
    samplePath.write_text(source, encoding='utf-8')

    violations = _checkFile(
        filename=samplePath,
        style=style,
        skipCheckingShortDocstrings=False,
        requireReturnSectionWhenReturningNothing=False,
    )
    actualMessages = [str(v) for v in violations]
    actualCodes = [msg.split(':', maxsplit=1)[0] for msg in actualMessages]
    assert actualCodes == expectedCodes

    for msg in actualMessages:
        if msg.startswith('DOC503:'):
            assert "Raised exceptions in the body: ['RuntimeError']." in msg


@pytest.mark.parametrize('style', ['numpy', 'google', 'sphinx'])
def testCliRaisedExceptionVariableMatchesInlineRaise(
        tmp_path: Path,
        style: str,
) -> None:
    docstring = _buildDocstring(style, ['RuntimeError'])
    source = (
        'def foo() -> None:\n'
        f'{docstring}'
        '    raise RuntimeError("An error occurred in foo")\n\n\n'
        'def bar() -> None:\n'
        f'{docstring}'
        '    exc = RuntimeError("An error occurred in bar")\n'
        '    exc.add_note("This is a rich exception with additional notes.")\n'
        '    raise exc\n'
    )
    samplePath = tmp_path / 'sample.py'
    samplePath.write_text(source, encoding='utf-8')

    result = CliRunner().invoke(
        cliMain,
        [
            f'--style={style}',
            '--exclude=',
            '--check-arg-defaults=False',
            '--require-return-section-when-returning-nothing=False',
            str(samplePath),
        ],
    )
    assert result.exit_code == 0, result.output


@pytest.mark.parametrize(
    ('funcSrc', 'expected'),
    [
        (
            'def f():\n'
            '    exc = RuntimeError("boom")\n'
            '    exc.add_note("ctx")\n'
            '    raise exc\n',
            ['RuntimeError'],
        ),
        (
            'async def f():\n    exc = RuntimeError("boom")\n    raise exc\n',
            ['RuntimeError'],
        ),
        (
            'def f():\n    exc = pkg.sub.CustomError("boom")\n    raise exc\n',
            ['pkg.sub.CustomError'],
        ),
        (
            'def f():\n    exc = CustomError.fromCode(404)\n    raise exc\n',
            ['CustomError.fromCode'],
        ),
        (
            'def f(tb):\n'
            '    exc = RuntimeError("boom").with_traceback(tb)\n'
            '    raise exc\n',
            ['RuntimeError'],
        ),
        (
            'def f(tb):\n'
            '    exc = RuntimeError("boom")\n'
            '    raise exc.with_traceback(tb)\n',
            ['RuntimeError'],
        ),
        (
            'def f(tb):\n'
            '    exc = RuntimeError("boom")\n'
            '    exc = exc.with_traceback(tb)\n'
            '    raise exc\n',
            ['RuntimeError'],
        ),
        (
            'def f():\n'
            '    exc = CustomError("boom")\n'
            '    exc = exc.withContext("detail")\n'
            '    raise exc\n',
            ['CustomError.withContext'],
        ),
        (
            'def f():\n'
            '    try:\n'
            '        step()\n'
            '    except ValueError as err:\n'
            '        exc = RuntimeError("wrapped")\n'
            '        exc.add_note("ctx")\n'
            '        raise exc from err\n',
            ['RuntimeError'],
        ),
        (
            'def f(exc: RuntimeError):\n'
            '    exc.add_note("ctx")\n'
            '    raise exc\n',
            ['RuntimeError'],
        ),
        (
            'def f(excCls: type[RuntimeError]):\n    raise excCls("boom")\n',
            ['RuntimeError'],
        ),
        (
            'def f():\n    exc: CustomError = buildError()\n    raise exc\n',
            ['CustomError'],
        ),
        (
            'def f():\n'
            '    exc: RuntimeError | ValueError = buildError()\n'
            '    raise exc\n',
            ['RuntimeError', 'ValueError'],
        ),
        (
            'def f():\n'
            '    exc: typing.Union[RuntimeError, ValueError] = buildError()\n'
            '    raise exc\n',
            ['RuntimeError', 'ValueError'],
        ),
        (
            'def f():\n'
            '    exc: Optional[RuntimeError] = buildError()\n'
            '    if exc is not None:\n'
            '        raise exc\n',
            ['RuntimeError'],
        ),
        (
            'def f():\n    exc: Final = RuntimeError("boom")\n    raise exc\n',
            ['RuntimeError'],
        ),
        (
            'def f():\n'
            '    exc: Annotated[RuntimeError, "meta"] = buildError()\n'
            '    raise exc\n',
            ['RuntimeError'],
        ),
        (
            'def f():\n'
            '    exc: "RuntimeError | KeyError" = buildError()\n'
            '    raise exc\n',
            ['KeyError', 'RuntimeError'],
        ),
        (
            'def f(cond: bool):\n'
            '    if cond:\n'
            '        exc = TypeError("bad type")\n'
            '    else:\n'
            '        exc = ValueError("bad value")\n'
            '    raise exc\n',
            ['TypeError', 'ValueError'],
        ),
        (
            'def f(cond: bool):\n'
            '    exc: Exception\n'
            '    if cond:\n'
            '        exc = TypeError("bad type")\n'
            '    else:\n'
            '        exc = ValueError("bad value")\n'
            '    raise exc\n',
            ['TypeError', 'ValueError'],
        ),
        (
            'def f(cond: bool) -> int:\n'
            '    if cond:\n'
            '        exc = ValueError("logged only")\n'
            '        return 0\n'
            '    else:\n'
            '        exc = RuntimeError("actually raised")\n'
            '    raise exc\n',
            ['RuntimeError'],
        ),
        (
            'def f():\n'
            '    exc = ValueError("stale")\n'
            '    exc = RuntimeError("actual")\n'
            '    raise exc\n',
            ['RuntimeError'],
        ),
        (
            'def f(cond: bool):\n'
            '    exc = TypeError("a") if cond else ValueError("b")\n'
            '    raise exc\n',
            ['TypeError', 'ValueError'],
        ),
        (
            'def f(cached: KeyError | None):\n'
            '    exc = cached or RuntimeError("fallback")\n'
            '    raise exc\n',
            ['KeyError', 'RuntimeError'],
        ),
        (
            'def f():\n'
            '    if (exc := RuntimeError("walrus")):\n'
            '        raise exc\n',
            ['RuntimeError'],
        ),
        (
            'def f():\n    raise (exc := RuntimeError("inline walrus"))\n',
            ['RuntimeError'],
        ),
        (
            'def f():\n'
            '    first = RuntimeError("first")\n'
            '    second = first\n'
            '    raise second\n',
            ['RuntimeError'],
        ),
        (
            'def f():\n'
            '    a, b = ValueError("a"), TypeError("b")\n'
            '    a, b = b, a\n'
            '    raise a\n',
            ['TypeError'],
        ),
        (
            'def f():\n    ErrorAlias = RuntimeError\n    raise ErrorAlias\n',
            ['ErrorAlias'],
        ),
        (
            'def f(items):\n'
            '    exc = None\n'
            '    for item in items:\n'
            '        if not item:\n'
            '            exc = ValueError("empty")\n'
            '            break\n'
            '    if exc is not None:\n'
            '        raise exc\n',
            ['ValueError'],
        ),
        (
            'def f(items):\n'
            '    exc = None\n'
            '    for item in items:\n'
            '        if not item:\n'
            '            exc = KeyError("missing")\n'
            '            continue\n'
            '    if exc is not None:\n'
            '        raise exc\n',
            ['KeyError'],
        ),
        (
            'def f():\n'
            '    try:\n'
            '        step1()\n'
            '    except ValueError as err:\n'
            '        log(err)\n'
            '    err = RuntimeError("step2")\n'
            '    raise err\n',
            ['RuntimeError'],
        ),
        (
            'def f():\n'
            '    try:\n'
            '        step1()\n'
            '    except IndexError:\n'
            '        if True:\n'
            '            try:\n'
            '                step2()\n'
            '            except KeyError:\n'
            '                pass\n'
            '            raise\n',
            ['IndexError'],
        ),
        (
            'def f(err):\n'
            '    match err:\n'
            '        case ValueError() as matched:\n'
            '            raise matched\n',
            ['ValueError'],
        ),
        (
            'def f(code: int):\n'
            '    match code:\n'
            '        case 1:\n'
            '            exc = ValueError("one")\n'
            '        case _:\n'
            '            exc = TypeError("other")\n'
            '    raise exc\n',
            ['TypeError', 'ValueError'],
        ),
        (
            'def f():\n'
            '    exc = RuntimeError("outer")\n'
            '    def inner():\n'
            '        exc = ValueError("inner")\n'
            '        raise exc\n'
            '    raise exc\n',
            ['RuntimeError'],
        ),
    ],
)
def testGetRaisedExceptionsResolvesVariables(
        funcSrc: str,
        expected: list[str],
) -> None:
    tree = ast.parse(funcSrc)
    node = tree.body[0]
    assert isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    assert getRaisedExceptions(node) == expected

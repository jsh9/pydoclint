import ast
from pathlib import Path

import pytest
from click.testing import CliRunner

from pydoclint.main import main
from pydoclint.utils.generic import specialEqual


@pytest.mark.parametrize(
    ('left', 'right', 'expected'),
    [
        ("str, default='#1f77b4'", "str, default='#ff0000'", False),
        ('str, default="#1f77b4"', 'str, default="#ff0000"', False),
        ("Literal['#yes']", "Literal['#no']", False),
        ("str, default=r'#yes'", "str, default=r'#no'", False),
        ("str, default='''#yes'''", "str, default='''#no'''", False),
        ("str, default='a\\'#yes'", "str, default='a\\'#no'", False),
        ("str, default='prefix#yes'", "str, default='prefix#no'", False),
        (
            "str, default='#yes' # comment",
            "str, default='#no' # comment",
            False,
        ),
        ("str, default='#yes'", 'str, default="#yes"', True),
        (
            "str, default='prefix\u2028#yes' # one",
            "str, default='prefix\u2028#no' # two",
            False,
        ),
        (
            "str, default='prefix\u2028#yes' # one",
            "str, default='prefix\u2028#yes' # two",
            True,
        ),
        ('int # noqa: E501', 'int', True),
        ('int # first', 'int # second', True),
        ("str, default='#yes' # first", "str, default='#yes' # second", True),
        ('list of int # comment', 'list of int', True),
        ('list[\n int\n] # comment', 'list[int]', True),
        ('str, default=', 'str, default=', True),
        ('str, default="""#unfinished', 'str, default="""#different', False),
    ],
)
def testQuotedHashes(left: str, right: str, expected: bool) -> None:
    assert specialEqual(left, right) is expected
    assert specialEqual(right, left) is expected


@pytest.mark.parametrize('wrongDefault', [True, False])
def testNativeColorDefault(tmp_path: Path, wrongDefault: bool) -> None:
    documented = '#ff0000' if wrongDefault else '#1f77b4'
    source = f'''def f(color: str = '#1f77b4') -> None:
    """Do things.

    Parameters
    ----------
    color : str, default='{documented}'
        The color.
    """
'''
    ast.parse(source)
    target = tmp_path / 'color.py'
    target.write_text(source)
    result = CliRunner().invoke(
        main,
        [
            '--check-arg-defaults=True',
            '--require-return-section-when-returning-nothing=False',
            str(target),
        ],
    )
    assert result.exit_code == (1 if wrongDefault else 0), result.output
    assert ('DOC105' in result.output) is wrongDefault, result.output

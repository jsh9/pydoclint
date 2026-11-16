from pathlib import Path

import pytest
from click.testing import CliRunner

from pydoclint.main import main


@pytest.mark.parametrize('style', ['numpy', 'google', 'sphinx'])
@pytest.mark.parametrize(
    ('yieldType', 'expectedCode'),
    [('int', None), ('str', 'DOC404'), (None, 'DOC402')],
)
def testCliYieldExpression(
        tmp_path: Path,
        style: str,
        yieldType: str | None,
        expectedCode: str | None,
) -> None:
    sections = {
        'numpy': f'Yields\n    ------\n    {yieldType}\n        An item.',
        'google': f'Yields:\n        {yieldType}: An item.',
        'sphinx': f':yields: An item.\n    :ytype: {yieldType}',
    }
    section = sections[style] if yieldType else 'An additional description.'
    source = (
        'from typing import Generator\n'
        'def generate() -> Generator[int, str, None]:\n'
        '    """Generate one item.\n\n'
        f'    {section}\n'
        '    """\n'
        '    received = yield 1\n'
    )
    samplePath = tmp_path / 'sample.py'
    samplePath.write_text(source, encoding='utf-8')
    result = CliRunner().invoke(
        main,
        [
            f'--style={style}',
            '--exclude=',
            '--check-arg-defaults=False',
            '--skip-checking-short-docstrings=False',
            str(samplePath),
        ],
    )
    assert result.exception is None or result.exit_code == 1
    assert 'DOC403' not in result.output
    if expectedCode is None:
        assert result.exit_code == 0
    else:
        assert result.exit_code == 1
        assert expectedCode in result.output

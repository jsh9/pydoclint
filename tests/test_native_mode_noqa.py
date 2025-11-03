from collections import Counter
from pathlib import Path

import pytest
from click.testing import CliRunner

from pydoclint.main import _checkFile
from pydoclint.main import main as cliMain

DATA_DIR = Path(__file__).parent / 'test_data' / 'noqa'
STYLES = ('google', 'numpy', 'sphinx')


@pytest.mark.parametrize('style', STYLES)
def testNativeModeDocstringNoqa(style: str) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'sample_{style}.py',
        style=style,
        nativeModeNoqaLocation='docstring',
    )

    messages = [str(v) for v in violations]
    codes = Counter(v.fullErrorCode for v in violations)

    assert all('funcDocstringComment' not in msg for msg in messages)
    assert any('funcDefinitionComment' in msg for msg in messages)
    assert codes == Counter({'DOC101': 2, 'DOC103': 2})


@pytest.mark.parametrize('style', STYLES)
def testNativeModeDefinitionNoqa(style: str) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'sample_{style}.py',
        style=style,
        nativeModeNoqaLocation='definition',
    )

    messages = [str(v) for v in violations]
    codes = Counter(v.fullErrorCode for v in violations)

    assert any('funcDocstringComment' in msg for msg in messages)

    funcDefinitionCodes = {
        v.fullErrorCode
        for v in violations
        if 'funcDefinitionComment' in str(v)
    }

    assert funcDefinitionCodes == {'DOC101'}
    assert codes == Counter({'DOC101': 3, 'DOC103': 2})


@pytest.mark.parametrize('style', STYLES)
def testNativeModeCliDocstringNoqa(style: str) -> None:
    runner = CliRunner()
    result = runner.invoke(
        cliMain,
        [
            '--quiet',
            '--check-arg-defaults=False',
            '--require-return-section-when-returning-nothing=False',
            f'--style={style}',
            '--native-mode-noqa-location=docstring',
            '--exclude=^$',
            str(DATA_DIR / f'sample_{style}.py'),
        ],
    )

    assert result.exit_code == 1
    assert 'funcDocstringComment' not in result.output
    assert 'funcDefinitionComment' in result.output


@pytest.mark.parametrize('style', STYLES)
def testNativeModeCliDefinitionNoqa(style: str) -> None:
    runner = CliRunner()
    result = runner.invoke(
        cliMain,
        [
            '--quiet',
            '--check-arg-defaults=False',
            '--require-return-section-when-returning-nothing=False',
            f'--style={style}',
            '--native-mode-noqa-location=definition',
            '--exclude=^$',
            str(DATA_DIR / f'sample_{style}.py'),
        ],
    )

    assert result.exit_code == 1
    assert 'funcDocstringComment' in result.output
    assert 'DOC103: Function `funcDefinitionComment`' not in result.output
    assert 'DOC101: Function `funcDefinitionComment`' in result.output

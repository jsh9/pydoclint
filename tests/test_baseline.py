import shutil
from pathlib import Path

import pytest

from pydoclint.baseline import (
    generateBaseline,
    parseBaseline,
    removeBaselineViolations,
)
from pydoclint.main import _checkPaths
from tests.test_main import DATA_DIR, pythonVersionBelow310

EXCLUDE_PATTERN = r'\.git|\.tox'
if pythonVersionBelow310():
    EXCLUDE_PATTERN = rf'{EXCLUDE_PATTERN}|py310\+'


@pytest.fixture
def baselineFile(tmp_path_factory) -> Path:
    return tmp_path_factory.mktemp('baseline') / 'test-baseline.txt'


@pytest.mark.parametrize(
    'style',
    ['google', 'numpy', 'sphinx'],
)
def testBaselineCreation(baselineFile, style: str):
    violationsInAllFiles = _checkPaths(
        paths=(DATA_DIR / style,),
        style=style,
        exclude=EXCLUDE_PATTERN,
    )
    generateBaseline(violationsInAllFiles, baselineFile)
    parsedBaseline = parseBaseline(baselineFile)
    (
        baselineRegenerationNeeded,
        clearedViolations,
    ) = removeBaselineViolations(parsedBaseline, violationsInAllFiles)
    assert baselineRegenerationNeeded is False
    assert clearedViolations == {}


badDocstringFunction = '''
def bad_docstring_func(arg1: str, arg2: list[int]) -> bool:
    """Something

    Returns
    -------
    bool
        Something else
    """
    return True
'''

expectedNewViolations = [
    'DOC101: Function `bad_docstring_func`: Docstring contains fewer arguments than in function signature.',
    'DOC103: Function `bad_docstring_func`: Docstring arguments are different from function arguments. '
    '(Or could be other formatting issues: https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
    'Arguments in the function signature but not in the docstring: [arg1: str, arg2: list[int]].',
]


@pytest.fixture(
    params=list(Path(DATA_DIR / 'numpy' / 'args').rglob('*.py'))[:5]
)
def violationsFile(request, tmp_path_factory) -> Path:
    tmpDir = tmp_path_factory.mktemp('new_violations')
    return shutil.copyfile(request.param, tmpDir / f'{request.param.name}')


def testBaselineNewViolations(baselineFile, violationsFile: Path):
    violationsInAllFiles = _checkPaths(
        (violationsFile,), exclude=EXCLUDE_PATTERN
    )
    generateBaseline(violationsInAllFiles, baselineFile)
    parsedBaseline = parseBaseline(baselineFile)

    with violationsFile.open('a', encoding='utf-8') as f:
        f.write(badDocstringFunction)

    newViolationsInAllFiles = _checkPaths(
        (violationsFile,), exclude=EXCLUDE_PATTERN
    )
    baselineRegenerationNeeded, clearedViolations = removeBaselineViolations(
        parsedBaseline, newViolationsInAllFiles
    )

    assert baselineRegenerationNeeded is False
    strViolations = [
        str(violation) for violation in list(clearedViolations.values())[0]
    ]
    assert strViolations == expectedNewViolations


@pytest.fixture
def tmpFile(tmp_path_factory) -> Path:
    return tmp_path_factory.mktemp('tmp') / 'code.py'


def testBaselineRegenerationNeeded(baselineFile, tmpFile: Path):
    with tmpFile.open('w', encoding='utf-8') as f:
        f.write(badDocstringFunction)

    violationsInAllFiles = _checkPaths((tmpFile,), exclude=EXCLUDE_PATTERN)
    generateBaseline(violationsInAllFiles, baselineFile)
    parsedBaseline = parseBaseline(baselineFile)

    with tmpFile.open('w'):
        pass

    newViolationsInAllFiles = _checkPaths((tmpFile,), exclude=EXCLUDE_PATTERN)
    baselineRegenerationNeeded, clearedViolations = removeBaselineViolations(
        parsedBaseline, newViolationsInAllFiles
    )

    assert baselineRegenerationNeeded is True
    assert clearedViolations == {}


def test_baseline_indent(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """
    Confirm round trip equality with a space or tab indent in the
    baseline file.

    Parameters
    ----------
    tmp_path : Path
        Temporary path.
    monkeypatch : pytest.MonkeyPatch
        Pytest monkeypatch fixture

    Returns
    -------
    None
    """

    code_file = tmp_path / 'code.py'
    baseline_spaces = tmp_path / 'baseline_spaces.txt'
    baseline_tabs = tmp_path / 'baseline_tabs.txt'

    code_file.write_text(badDocstringFunction)
    violations = _checkPaths((str(code_file),), exclude=EXCLUDE_PATTERN)

    generateBaseline(violations, baseline_spaces)

    monkeypatch.setattr('pydoclint.baseline.INDENT', '\t')
    generateBaseline(violations, baseline_tabs)

    assert baseline_spaces.read_text().splitlines()[1].startswith('    ')
    assert baseline_tabs.read_text().splitlines()[1].startswith('\t')

    key = code_file.as_posix()
    space_parsed = sorted(parseBaseline(baseline_spaces)[key])
    tab_parsed = sorted(parseBaseline(baseline_tabs)[key])
    violations_str = sorted(str(v) for v in violations[key])

    assert space_parsed == tab_parsed == violations_str

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
    'DOC101: Function `bad_docstring_func`: Docstring contains fewer arguments than in function signature. ',
    'DOC109: Function `bad_docstring_func`: The option `--arg-type-hints-in-docstring` is `True` '
    'but there are no type hints in the docstring arg list ',
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

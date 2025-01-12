import shutil
import sys
from pathlib import Path

import pytest

from pydoclint.baseline import (
    calcUnfixedBaselineViolationsAndRemainingViolations,
    generateBaseline,
    parseBaseline,
    reEvaluateBaseline,
)
from pydoclint.main import _checkPaths
from pydoclint.utils.violation import Violation
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
        unfixedBaselineViolationsInAllFiles,
        remainingViolationsInAllFiles,
    ) = reEvaluateBaseline(parsedBaseline, violationsInAllFiles)
    assert baselineRegenerationNeeded is False
    assert all(
        len(violations) == 0
        for filename, violations in remainingViolationsInAllFiles.items()
    )
    # In the future, this assertion could break if we add new files
    # to DATA_DIR. But it's good that this could act as a sanity check.
    if sys.version_info < (3, 10):
        assert len(unfixedBaselineViolationsInAllFiles) == 26
    else:
        assert len(unfixedBaselineViolationsInAllFiles) == 32


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

twoFunctionsWithBadDocstrings = '''
def bad_docstring_func(arg1: str, arg2: list[int]) -> bool:
    """Something

    Returns
    -------
    bool
        Something else
    """
    return True

def func2(arg1: str, arg2: list[int]) -> int:
    """Something

    Parameters
    ----------
    arg1 : bool
        Arg 1

    Returns
    -------
    int
        The return value
    """
    return True
'''


onlyOneFunctionWithBadDocstring = '''
def bad_docstring_func(arg1: str, arg2: list[int]) -> bool:
    """Something

    Returns
    -------
    bool
        Something else
    """
    return True

def func2(arg1: str, arg2: list[int]) -> int:
    """Something

    Parameters
    ----------
    arg1 : str
        Arg 1
    arg2 : list[int]
        Arg 2

    Returns
    -------
    int
        The return value
    """
    return True
'''


someViolationsFixedButNewViolationsOccur = '''
def bad_docstring_func(arg1: str, arg2: list[int]) -> bool:
    """Something

    Returns
    -------
    bool
        Something else
    """
    if not isinstance(arg1, str):
        raise ValueError('')

    return True

def func2(arg1: str, arg2: list[int]) -> int:
    """Something

    Parameters
    ----------
    arg1 : str
        Arg 1
    arg2 : list[int]
        Arg 2

    Returns
    -------
    int
        The return value
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


def testBaselineNewViolations(baselineFile: Path, violationsFile: Path):
    violationsInAllFiles: dict[str, list[Violation]] = _checkPaths(
        (violationsFile.as_posix(),), exclude=EXCLUDE_PATTERN
    )
    generateBaseline(violationsInAllFiles, baselineFile)
    parsedBaseline: dict[str, list[str]] = parseBaseline(baselineFile)

    with violationsFile.open('a', encoding='utf-8') as f:
        f.write(badDocstringFunction)

    newViolationsInAllFiles: dict[str, list[Violation]] = _checkPaths(
        (violationsFile.as_posix(),), exclude=EXCLUDE_PATTERN
    )
    (
        baselineRegenerationNeeded,
        unfixedBaselineViolationsInAllFiles,
        remainingViolationsInAllFiles,
    ) = reEvaluateBaseline(parsedBaseline, newViolationsInAllFiles)

    # Because we didn't fix any baseline violations:
    assert baselineRegenerationNeeded is False
    assert unfixedBaselineViolationsInAllFiles == parsedBaseline

    strViolations = [
        str(violation)
        for violation in list(remainingViolationsInAllFiles.values())[0]
    ]
    assert strViolations == expectedNewViolations


@pytest.fixture
def tmpFile(tmp_path_factory) -> Path:
    return tmp_path_factory.mktemp('tmp') / 'code.py'


def testSomeViolationsAreFixed(baselineFile: Path, tmpFile: Path):
    with tmpFile.open('w', encoding='utf-8') as f:
        f.write(twoFunctionsWithBadDocstrings)

    violationsInAllFiles: dict[str, list[Violation]] = _checkPaths(
        (tmpFile.as_posix(),), exclude=EXCLUDE_PATTERN
    )
    generateBaseline(violationsInAllFiles, baselineFile)
    parsedBaseline: dict[str, list[str]] = parseBaseline(baselineFile)

    with tmpFile.open('w', encoding='utf-8') as f:
        # This is to simulate that some violations are fixed
        f.write(onlyOneFunctionWithBadDocstring)

    newViolationsInAllFiles = _checkPaths(
        (tmpFile.as_posix(),), exclude=EXCLUDE_PATTERN
    )
    (
        baselineRegenerationNeeded,
        unfixedBaselineViolationsInAllFiles,
        remainingViolationsInAllFiles,
    ) = reEvaluateBaseline(parsedBaseline, newViolationsInAllFiles)

    assert baselineRegenerationNeeded is True
    assert unfixedBaselineViolationsInAllFiles == {
        tmpFile.as_posix(): expectedNewViolations
    }
    assert remainingViolationsInAllFiles == {tmpFile.as_posix(): []}


def testSomeViolationsAreFixedButNewViolationsOccur(
        baselineFile: Path,
        tmpFile: Path,
):
    with tmpFile.open('w', encoding='utf-8') as f:
        f.write(twoFunctionsWithBadDocstrings)

    violationsInAllFiles: dict[str, list[Violation]] = _checkPaths(
        (tmpFile.as_posix(),), exclude=EXCLUDE_PATTERN
    )
    generateBaseline(violationsInAllFiles, baselineFile)
    parsedBaseline: dict[str, list[str]] = parseBaseline(baselineFile)

    assert parsedBaseline == {
        tmpFile.as_posix(): expectedNewViolations
        + [
            'DOC101: Function `func2`: Docstring contains fewer arguments than in function signature.',
            'DOC103: Function `func2`: Docstring arguments are different'
            ' from function arguments. (Or could be other formatting'
            ' issues: https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ).'
            ' Arguments in the function signature but not in the docstring: [arg2: list[int]].',
        ]
    }

    with tmpFile.open('w', encoding='utf-8') as f:
        # This is to simulate that some violations are fixed, but
        # additional violations occur
        f.write(someViolationsFixedButNewViolationsOccur)

    newViolationsInAllFiles = _checkPaths(
        (tmpFile.as_posix(),), exclude=EXCLUDE_PATTERN
    )
    (
        baselineRegenerationNeeded,
        unfixedBaselineViolationsInAllFiles,
        remainingViolationsInAllFiles,
    ) = reEvaluateBaseline(parsedBaseline, newViolationsInAllFiles)

    assert baselineRegenerationNeeded is True
    assert unfixedBaselineViolationsInAllFiles == {
        tmpFile.as_posix(): expectedNewViolations
    }

    additionalViolations = [
        'DOC501: Function `bad_docstring_func` has "raise" statements, but'
        ' the docstring does not have a "Raises" section',
        'DOC503: Function `bad_docstring_func` exceptions in the "Raises"'
        ' section in the docstring do not match those in the function body.'
        ' Raised exceptions in the docstring: []. Raised'
        " exceptions in the body: ['ValueError'].",
    ]

    assert len(remainingViolationsInAllFiles.keys()) == 1
    assert list(remainingViolationsInAllFiles.keys())[0] == tmpFile.as_posix()
    assert [
        str(_) for _ in remainingViolationsInAllFiles[tmpFile.as_posix()]
    ] == additionalViolations


def testBaselineIndent(
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

    codeFile = tmp_path / 'code.py'
    baselineSpaces = tmp_path / 'baseline_spaces.txt'
    baselineTabs = tmp_path / 'baseline_tabs.txt'

    codeFile.write_text(badDocstringFunction)
    violations = _checkPaths((str(codeFile),), exclude=EXCLUDE_PATTERN)

    generateBaseline(violations, baselineSpaces)

    monkeypatch.setattr('pydoclint.baseline.INDENT', '\t')
    generateBaseline(violations, baselineTabs)

    assert baselineSpaces.read_text().splitlines()[1].startswith('    ')
    assert baselineTabs.read_text().splitlines()[1].startswith('\t')

    key = codeFile.as_posix()
    spaceParsed = sorted(parseBaseline(baselineSpaces)[key])
    tabParsed = sorted(parseBaseline(baselineTabs)[key])
    violationsStr = sorted(str(v) for v in violations[key])

    assert spaceParsed == tabParsed == violationsStr


@pytest.mark.parametrize(
    'baselineViolations, actualViolations, expectedUnfixed, expectedRemaining',
    [
        (
            [],
            [],
            [],
            [],
        ),
        (  # No baseline to begin with; new violations found
            [],
            [
                Violation(line=0, code=201, msgPrefix='', msgPostfix=''),
                Violation(line=0, code=202, msgPrefix='', msgPostfix=''),
                Violation(line=0, code=203, msgPrefix='', msgPostfix=''),
            ],
            [],
            [
                Violation(line=0, code=201, msgPrefix='', msgPostfix=''),
                Violation(line=0, code=202, msgPrefix='', msgPostfix=''),
                Violation(line=0, code=203, msgPrefix='', msgPostfix=''),
            ],
        ),
        (  # Nothing in baseline is fixed, and no new violations found
            [
                'DOC201: does not have a return section in docstring',
                'DOC202: has a return section in docstring, but there are no return statements or annotations',
                'DOC203: return type(s) in docstring not consistent with the return annotation.',
            ],
            [
                Violation(line=0, code=201, msgPrefix='', msgPostfix=''),
                Violation(line=0, code=202, msgPrefix='', msgPostfix=''),
                Violation(line=0, code=203, msgPrefix='', msgPostfix=''),
            ],
            [
                'DOC201: does not have a return section in docstring',
                'DOC202: has a return section in docstring, but there are no return statements or annotations',
                'DOC203: return type(s) in docstring not consistent with the return annotation.',
            ],
            [],
        ),
        (  # Nothing in baseline is fixed, and new violations found
            [
                'DOC201: does not have a return section in docstring',
                'DOC202: has a return section in docstring, but there are no return statements or annotations',
                'DOC203: return type(s) in docstring not consistent with the return annotation.',
            ],
            [
                Violation(line=0, code=201, msgPrefix='', msgPostfix=''),
                Violation(line=0, code=202, msgPrefix='', msgPostfix=''),
                Violation(line=0, code=203, msgPrefix='', msgPostfix=''),
                Violation(line=0, code=501, msgPrefix='', msgPostfix=''),
                Violation(line=0, code=502, msgPrefix='', msgPostfix=''),
            ],
            [
                'DOC201: does not have a return section in docstring',
                'DOC202: has a return section in docstring, but there are no return statements or annotations',
                'DOC203: return type(s) in docstring not consistent with the return annotation.',
            ],
            [
                Violation(line=0, code=501, msgPrefix='', msgPostfix=''),
                Violation(line=0, code=502, msgPrefix='', msgPostfix=''),
            ],
        ),
        (  # Everything in baseline is fixed, and new violations found
            [
                'DOC201: does not have a return section in docstring',
                'DOC202: has a return section in docstring, but there are no return statements or annotations',
                'DOC203: return type(s) in docstring not consistent with the return annotation.',
            ],
            [
                Violation(line=0, code=501, msgPrefix='', msgPostfix=''),
                Violation(line=0, code=502, msgPrefix='', msgPostfix=''),
            ],
            [],
            [
                Violation(line=0, code=501, msgPrefix='', msgPostfix=''),
                Violation(line=0, code=502, msgPrefix='', msgPostfix=''),
            ],
        ),
        (  # Everything in baseline is fixed, and no new violations found
            [
                'DOC201: does not have a return section in docstring',
                'DOC202: has a return section in docstring, but there are no return statements or annotations',
                'DOC203: return type(s) in docstring not consistent with the return annotation.',
            ],
            [],
            [],
            [],
        ),
        (  # Some violations in baseline are fixed, and new violations found
            [
                'DOC201: does not have a return section in docstring',
                'DOC202: has a return section in docstring, but there are no return statements or annotations',
                'DOC203: return type(s) in docstring not consistent with the return annotation.',
            ],
            [
                Violation(line=0, code=203, msgPrefix='', msgPostfix=''),
                Violation(line=0, code=501, msgPrefix='', msgPostfix=''),
                Violation(line=0, code=502, msgPrefix='', msgPostfix=''),
            ],
            [
                'DOC203: return type(s) in docstring not consistent with the return annotation.',
            ],
            [
                Violation(line=0, code=501, msgPrefix='', msgPostfix=''),
                Violation(line=0, code=502, msgPrefix='', msgPostfix=''),
            ],
        ),
        (  # Everything in baseline is fixed, and new violations found
            [
                'DOC201: does not have a return section in docstring',
                'DOC202: has a return section in docstring, but there are no return statements or annotations',
                'DOC203: return type(s) in docstring not consistent with the return annotation.',
            ],
            [
                Violation(line=0, code=501, msgPrefix='', msgPostfix=''),
                Violation(line=0, code=502, msgPrefix='', msgPostfix=''),
            ],
            [],
            [
                Violation(line=0, code=501, msgPrefix='', msgPostfix=''),
                Violation(line=0, code=502, msgPrefix='', msgPostfix=''),
            ],
        ),
    ],
)
def testCalcUnfixedBaselineViolationsAndRemainingViolations(
        baselineViolations: list[str],
        actualViolations: list[Violation],
        expectedUnfixed: list[str],
        expectedRemaining: list[Violation],
) -> None:
    unfixed, remaining = calcUnfixedBaselineViolationsAndRemainingViolations(
        baselineViolations=baselineViolations,
        actualViolations=actualViolations,
    )
    assert unfixed == expectedUnfixed
    assert remaining == expectedRemaining

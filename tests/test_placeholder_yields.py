from pathlib import Path

import pytest

from pydoclint.main import _checkFile

DATA_DIR = Path(__file__).parent / 'test_data'
FIXTURE_DIR = DATA_DIR / 'edge_cases/37_placeholder_yield_types'
ALL_STYLES = ['google', 'numpy', 'sphinx']


@pytest.mark.parametrize('style', ALL_STYLES)
@pytest.mark.parametrize(
    'bodyKind', ['real', 'stub', 'abstract', 'placeholder']
)
@pytest.mark.parametrize('checkYieldTypes', [False, True])
@pytest.mark.parametrize('mismatched', [False, True])
def testPlaceholderYieldTypes(
        tmp_path: Path,
        style: str,
        bodyKind: str,
        checkYieldTypes: bool,
        mismatched: bool,
) -> None:
    source = (FIXTURE_DIR / f'{style}.py').read_text()
    if mismatched:
        source = source.replace('[int]', '[str]')

    if bodyKind != 'real':
        source = source.replace('yield 1', '...')

    if bodyKind == 'abstract':
        source = source.replace('async def ', '@abstractmethod\nasync def ')
        source = source.replace('\ndef ', '\n@abstractmethod\ndef ')

    filename = tmp_path / ('cases.pyi' if bodyKind == 'stub' else 'cases.py')
    filename.write_text(source)
    violations = _checkFile(
        filename=filename,
        style=style,
        checkYieldTypes=checkYieldTypes,
    )
    if bodyKind == 'placeholder':
        # An ordinary .py function with ... has no evidence of yielding.
        expected = [403, 403, 201, 403, 201, 403, 201, 403, 201, 403]
    else:
        expected = [404] * 6 if mismatched and checkYieldTypes else []

    assert [violation.code for violation in violations] == expected


@pytest.mark.parametrize('style', ALL_STYLES)
@pytest.mark.parametrize('bodyKind', ['stub', 'abstract'])
@pytest.mark.parametrize(
    'requireYieldSectionWhenYieldingNothing', [False, True]
)
def testPlaceholderYieldSectionRequirements(
        tmp_path: Path,
        style: str,
        bodyKind: str,
        requireYieldSectionWhenYieldingNothing: bool,
) -> None:
    source = (FIXTURE_DIR / f'{style}.pyi').read_text()
    if bodyKind == 'abstract':
        source = source.replace('\ndef ', '\n@abstractmethod\ndef ')

    filename = tmp_path / ('cases.pyi' if bodyKind == 'stub' else 'cases.py')
    filename.write_text(source)
    violations = _checkFile(
        filename=filename,
        style=style,
        skipCheckingShortDocstrings=False,
        requireYieldSectionWhenYieldingNothing=(
            requireYieldSectionWhenYieldingNothing
        ),
    )
    # Returns-only iterators, missing Yields, and explicit None yields retain
    # their behavior. Only stubs reject the non-generator's Yields section.
    expected = [403] if bodyKind == 'stub' else []
    assert [violation.code for violation in violations] == expected


@pytest.mark.parametrize('style', ALL_STYLES)
@pytest.mark.parametrize('mismatched', [False, True])
def testAbstractIteratorWithReturnBody(
        tmp_path: Path,
        style: str,
        mismatched: bool,
) -> None:
    source = (DATA_DIR / f'{style}/abstract_method/cases.py').read_text()
    if mismatched:
        source = source.replace('Iterator[str]', 'Iterator[int]')

    filename = tmp_path / 'cases.py'
    filename.write_text(source)
    violations = _checkFile(filename=filename, style=style)
    relevantCodes = [
        violation.code
        for violation in violations
        if 'abstractIteratorThatReturns' in str(violation)
    ]
    assert relevantCodes == ([201, 404] if mismatched else [201])


@pytest.mark.parametrize('style', ALL_STYLES)
@pytest.mark.parametrize(
    'requireYieldSectionWhenYieldingNothing', [False, True]
)
def testAbstractMethodsWithRealYieldBodies(
        tmp_path: Path,
        style: str,
        requireYieldSectionWhenYieldingNothing: bool,
) -> None:
    source = (DATA_DIR / f'{style}/no_yield_section/cases.py').read_text()
    source = source.replace('def ', '@abstractmethod\ndef ')
    filename = tmp_path / 'cases.py'
    filename.write_text(source)
    violations = _checkFile(
        filename=filename,
        style=style,
        requireYieldSectionWhenYieldingNothing=(
            requireYieldSectionWhenYieldingNothing
        ),
    )
    # Actual yield statements still drive missing-section checks, including
    # the None-yield option and the separate yield-and-return path.
    expected = [402, 404] * (
        3 if requireYieldSectionWhenYieldingNothing else 1
    )
    assert [violation.code for violation in violations] == expected

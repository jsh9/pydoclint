import itertools
from pathlib import Path
from typing import Dict, List

import pytest

from pydoclint.main import _checkFile

THIS_DIR = Path(__file__).parent
DATA_DIR = THIS_DIR / 'data'


expectedViolations_True_True = [
    'DOC101: Function `func1_2`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Function `func1_2`: Docstring arguments are different from function '
    'arguments. Arguments in the function signature but not in the docstring: '
    '[arg1: int, arg2: float].',
    'DOC101: Function `func1_3`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Function `func1_3`: Docstring arguments are different from function '
    'arguments. Arguments in the function signature but not in the docstring: '
    '[arg1: str, arg2: list[int]].',
    'DOC102: Function `func1_6`: Docstring contains more arguments than in '
    'function signature. ',
    'DOC103: Function `func1_6`: Docstring arguments are different from function '
    'arguments. Arguments in the docstring but not in the function signature: '
    '[arg1: int].',
    'DOC101: Function `func2`: Docstring contains fewer arguments than in function '
    'signature. ',
    'DOC103: Function `func2`: Docstring arguments are different from function '
    'arguments. Arguments in the function signature but not in the docstring: '
    '[arg2: float | int | None].',
    'DOC102: Function `func3`: Docstring contains more arguments than in function '
    'signature. ',
    'DOC103: Function `func3`: Docstring arguments are different from function '
    'arguments. Arguments in the docstring but not in the function signature: '
    '[arg3: Optional[Union[float, int, str]]].',
    'DOC104: Function `func4`: Arguments are the same in the docstring and the '
    'function signature, but are in a different order. ',
    'DOC105: Function `func5`: Argument names match, but type hints do not match ',
    'DOC104: Function `func6`: Arguments are the same in the docstring and the '
    'function signature, but are in a different order. ',
    'DOC105: Function `func6`: Argument names match, but type hints do not match ',
    'DOC101: Function `func72`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Function `func72`: Docstring arguments are different from function '
    'arguments. Arguments in the function signature but not in the docstring: '
    '[arg3: list, arg4: tuple, arg5: dict].',
]

expectedViolations_False_True = [
    'DOC101: Function `func1_2`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Function `func1_2`: Docstring arguments are different from function '
    'arguments. Arguments in the function signature but not in the docstring: '
    '[arg1: int, arg2: float].',
    'DOC101: Function `func1_3`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Function `func1_3`: Docstring arguments are different from function '
    'arguments. Arguments in the function signature but not in the docstring: '
    '[arg1: str, arg2: list[int]].',
    'DOC102: Function `func1_6`: Docstring contains more arguments than in '
    'function signature. ',
    'DOC103: Function `func1_6`: Docstring arguments are different from function '
    'arguments. Arguments in the docstring but not in the function signature: '
    '[arg1: int].',
    'DOC101: Function `func2`: Docstring contains fewer arguments than in function '
    'signature. ',
    'DOC103: Function `func2`: Docstring arguments are different from function '
    'arguments. Arguments in the function signature but not in the docstring: '
    '[arg2: float | int | None].',
    'DOC102: Function `func3`: Docstring contains more arguments than in function '
    'signature. ',
    'DOC103: Function `func3`: Docstring arguments are different from function '
    'arguments. Arguments in the docstring but not in the function signature: '
    '[arg3: Optional[Union[float, int, str]]].',
    'DOC104: Function `func4`: Arguments are the same in the docstring and the '
    'function signature, but are in a different order. ',
    'DOC104: Function `func6`: Arguments are the same in the docstring and the '
    'function signature, but are in a different order. ',
    'DOC101: Function `func72`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Function `func72`: Docstring arguments are different from function '
    'arguments. Arguments in the function signature but not in the docstring: '
    '[arg3: list, arg4: tuple, arg5: dict].',
]

expectedViolations_True_False = [
    'DOC101: Function `func1_2`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Function `func1_2`: Docstring arguments are different from function '
    'arguments. Arguments in the function signature but not in the docstring: '
    '[arg1: int, arg2: float].',
    'DOC101: Function `func1_3`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Function `func1_3`: Docstring arguments are different from function '
    'arguments. Arguments in the function signature but not in the docstring: '
    '[arg1: str, arg2: list[int]].',
    'DOC102: Function `func1_6`: Docstring contains more arguments than in '
    'function signature. ',
    'DOC103: Function `func1_6`: Docstring arguments are different from function '
    'arguments. Arguments in the docstring but not in the function signature: '
    '[arg1: int].',
    'DOC101: Function `func2`: Docstring contains fewer arguments than in function '
    'signature. ',
    'DOC103: Function `func2`: Docstring arguments are different from function '
    'arguments. Arguments in the function signature but not in the docstring: '
    '[arg2: float | int | None].',
    'DOC102: Function `func3`: Docstring contains more arguments than in function '
    'signature. ',
    'DOC103: Function `func3`: Docstring arguments are different from function '
    'arguments. Arguments in the docstring but not in the function signature: '
    '[arg3: Optional[Union[float, int, str]]].',
    'DOC105: Function `func5`: Argument names match, but type hints do not match ',
    'DOC105: Function `func6`: Argument names match, but type hints do not match ',
    'DOC101: Function `func72`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Function `func72`: Docstring arguments are different from function '
    'arguments. Arguments in the function signature but not in the docstring: '
    '[arg3: list, arg4: tuple, arg5: dict].',
]

expectedViolations_False_False = [
    'DOC101: Function `func1_2`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Function `func1_2`: Docstring arguments are different from function '
    'arguments. Arguments in the function signature but not in the docstring: '
    '[arg1: int, arg2: float].',
    'DOC101: Function `func1_3`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Function `func1_3`: Docstring arguments are different from function '
    'arguments. Arguments in the function signature but not in the docstring: '
    '[arg1: str, arg2: list[int]].',
    'DOC102: Function `func1_6`: Docstring contains more arguments than in '
    'function signature. ',
    'DOC103: Function `func1_6`: Docstring arguments are different from function '
    'arguments. Arguments in the docstring but not in the function signature: '
    '[arg1: int].',
    'DOC101: Function `func2`: Docstring contains fewer arguments than in function '
    'signature. ',
    'DOC103: Function `func2`: Docstring arguments are different from function '
    'arguments. Arguments in the function signature but not in the docstring: '
    '[arg2: float | int | None].',
    'DOC102: Function `func3`: Docstring contains more arguments than in function '
    'signature. ',
    'DOC103: Function `func3`: Docstring arguments are different from function '
    'arguments. Arguments in the docstring but not in the function signature: '
    '[arg3: Optional[Union[float, int, str]]].',
    'DOC101: Function `func72`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Function `func72`: Docstring arguments are different from function '
    'arguments. Arguments in the function signature but not in the docstring: '
    '[arg3: list, arg4: tuple, arg5: dict].',
]

expectedViolationsLookup: Dict[str, List[str]] = {
    'true_true': expectedViolations_True_True,
    'true_false': expectedViolations_True_False,
    'false_true': expectedViolations_False_True,
    'false_false': expectedViolations_False_False,
}

optionDictLookup: Dict[str, Dict[str, bool]] = {
    'true_true': {'checkTypeHint': True, 'checkArgOrder': True},
    'true_false': {'checkTypeHint': True, 'checkArgOrder': False},
    'false_true': {'checkTypeHint': False, 'checkArgOrder': True},
    'false_false': {'checkTypeHint': False, 'checkArgOrder': False},
}

options = [
    'true_true',
    'true_false',
    'false_true',
    'false_false',
]


@pytest.mark.parametrize(
    'filename, option',
    list(
        itertools.product(
            ['function.py', 'classmethod.py', 'method.py', 'staticmethod.py'],
            options,
        ),
    ),
)
def testArguments(
        filename: str,
        option: str,
) -> None:
    optionDict: Dict[str, bool] = optionDictLookup[option]
    expectedViolations: List[str] = expectedViolationsLookup[option]

    violations = _checkFile(
        filename=DATA_DIR / f'args/{filename}',
        checkTypeHint=optionDict['checkTypeHint'],
        checkArgOrder=optionDict['checkArgOrder'],
    )
    assert list(map(str, violations)) == expectedViolations


@pytest.mark.parametrize(
    'filename',
    ['function.py', 'classmethod.py', 'method.py', 'staticmethod.py'],
)
def testReturns(filename: str) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'returns/{filename}',
        skipCheckingShortDocstrings=False,
    )
    expectedViolations: List[str] = [
        'DOC201: Function `func1_3` does not have a return section in docstring ',
        'DOC201: Function `func1_5` does not have a return section in docstring ',
        'DOC201: Function `func1_6` does not have a return section in docstring ',
        'DOC101: Function `func2`: Docstring contains fewer arguments than in function '
        'signature. ',
        'DOC103: Function `func2`: Docstring arguments are different from function '
        'arguments. Arguments in the function signature but not in the docstring: '
        '[arg2: float, arg3: str]. Arguments in the docstring but not in the function '
        'signature: [arg1: int].',
        'DOC201: Function `func52` does not have a return section in docstring ',
        'DOC202: Function `func6` has a return section in docstring, but there are no '
        'return statements or annotations ',
        'DOC202: Function `func7` has a return section in docstring, but there are no '
        'return statements or annotations ',
    ]
    assert list(map(str, violations)) == expectedViolations


expected_True = [
    'DOC101: Function `func3`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Function `func3`: Docstring arguments are different from function '
    'arguments. Arguments in the function signature but not in the docstring: '
    '[arg1: , arg2: , arg3: ]. Arguments in the docstring but not in the function '
    'signature: [var1: int, var2: str].',
    'DOC201: Function `func3` does not have a return section in docstring ',
]

expected_False = [
    'DOC101: Function `func1`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Function `func1`: Docstring arguments are different from function '
    'arguments. Arguments in the function signature but not in the docstring: '
    '[arg1: , arg2: , arg3: ].',
    'DOC201: Function `func1` does not have a return section in docstring ',
    'DOC101: Function `func2`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Function `func2`: Docstring arguments are different from function '
    'arguments. Arguments in the function signature but not in the docstring: '
    '[arg1: , arg2: , arg3: ].',
    'DOC201: Function `func2` does not have a return section in docstring ',
    'DOC101: Function `func3`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Function `func3`: Docstring arguments are different from function '
    'arguments. Arguments in the function signature but not in the docstring: '
    '[arg1: , arg2: , arg3: ]. Arguments in the docstring but not in the function '
    'signature: [var1: int, var2: str].',
    'DOC201: Function `func3` does not have a return section in docstring ',
]


@pytest.mark.parametrize(
    'skipCheckingShortDocstrings, expected',
    [(True, expected_True), (False, expected_False)],
)
def testSkipCheckingShortDocstrings(
        skipCheckingShortDocstrings: bool,
        expected: List[str],
) -> None:
    violations = _checkFile(
        filename=DATA_DIR / 'short_docstrings/cases.py',
        skipCheckingShortDocstrings=skipCheckingShortDocstrings,
    )
    assert list(map(str, violations)) == expected

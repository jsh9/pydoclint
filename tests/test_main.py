import copy
import itertools
from pathlib import Path
from typing import Dict, List

import pytest

from pydoclint.main import _checkFile

THIS_DIR = Path(__file__).parent
DATA_DIR = THIS_DIR / 'data'


expectedViolations_True_True = [
    'DOC101: Method `MyClass.func1_3`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func1_3`: Docstring arguments are different from '
    'function arguments. (Or did you miss the space between the argument name and '
    'the ":" in the docstring?). Arguments in the function signature but not in '
    'the docstring: [arg1: str, arg2: list[int]].',
    'DOC102: Method `MyClass.func1_6`: Docstring contains more arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func1_6`: Docstring arguments are different from '
    'function arguments. (Or did you miss the space between the argument name and '
    'the ":" in the docstring?). Arguments in the docstring but not in the '
    'function signature: [arg1: int].',
    'DOC101: Method `MyClass.func2`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func2`: Docstring arguments are different from '
    'function arguments. (Or did you miss the space between the argument name and '
    'the ":" in the docstring?). Arguments in the function signature but not in '
    'the docstring: [arg2: float | int | None].',
    'DOC102: Method `MyClass.func3`: Docstring contains more arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func3`: Docstring arguments are different from '
    'function arguments. (Or did you miss the space between the argument name and '
    'the ":" in the docstring?). Arguments in the docstring but not in the '
    'function signature: [arg3: Optional[Union[float, int, str]]].',
    'DOC104: Method `MyClass.func4`: Arguments are the same in the docstring and '
    'the function signature, but are in a different order. ',
    'DOC105: Method `MyClass.func5`: Argument names match, but type hints do not '
    'match ',
    'DOC104: Method `MyClass.func6`: Arguments are the same in the docstring and '
    'the function signature, but are in a different order. ',
    'DOC105: Method `MyClass.func6`: Argument names match, but type hints do not '
    'match ',
    'DOC101: Function `func72`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Function `func72`: Docstring arguments are different from function '
    'arguments. (Or did you miss the space between the argument name and the ":" '
    'in the docstring?). Arguments in the function signature but not in the '
    'docstring: [arg3: list, arg4: tuple, arg5: dict].',
]

expectedViolations_False_True = [
    'DOC101: Method `MyClass.func1_3`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func1_3`: Docstring arguments are different from '
    'function arguments. (Or did you miss the space between the argument name and '
    'the ":" in the docstring?). Arguments in the function signature but not in '
    'the docstring: [arg1: str, arg2: list[int]].',
    'DOC102: Method `MyClass.func1_6`: Docstring contains more arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func1_6`: Docstring arguments are different from '
    'function arguments. (Or did you miss the space between the argument name and '
    'the ":" in the docstring?). Arguments in the docstring but not in the '
    'function signature: [arg1: int].',
    'DOC101: Method `MyClass.func2`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func2`: Docstring arguments are different from '
    'function arguments. (Or did you miss the space between the argument name and '
    'the ":" in the docstring?). Arguments in the function signature but not in '
    'the docstring: [arg2: float | int | None].',
    'DOC102: Method `MyClass.func3`: Docstring contains more arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func3`: Docstring arguments are different from '
    'function arguments. (Or did you miss the space between the argument name and '
    'the ":" in the docstring?). Arguments in the docstring but not in the '
    'function signature: [arg3: Optional[Union[float, int, str]]].',
    'DOC104: Method `MyClass.func4`: Arguments are the same in the docstring and '
    'the function signature, but are in a different order. ',
    'DOC104: Method `MyClass.func6`: Arguments are the same in the docstring and '
    'the function signature, but are in a different order. ',
    'DOC101: Function `func72`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Function `func72`: Docstring arguments are different from function '
    'arguments. (Or did you miss the space between the argument name and the ":" '
    'in the docstring?). Arguments in the function signature but not in the '
    'docstring: [arg3: list, arg4: tuple, arg5: dict].',
]

expectedViolations_True_False = [
    'DOC101: Method `MyClass.func1_3`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func1_3`: Docstring arguments are different from '
    'function arguments. (Or did you miss the space between the argument name and '
    'the ":" in the docstring?). Arguments in the function signature but not in '
    'the docstring: [arg1: str, arg2: list[int]].',
    'DOC102: Method `MyClass.func1_6`: Docstring contains more arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func1_6`: Docstring arguments are different from '
    'function arguments. (Or did you miss the space between the argument name and '
    'the ":" in the docstring?). Arguments in the docstring but not in the '
    'function signature: [arg1: int].',
    'DOC101: Method `MyClass.func2`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func2`: Docstring arguments are different from '
    'function arguments. (Or did you miss the space between the argument name and '
    'the ":" in the docstring?). Arguments in the function signature but not in '
    'the docstring: [arg2: float | int | None].',
    'DOC102: Method `MyClass.func3`: Docstring contains more arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func3`: Docstring arguments are different from '
    'function arguments. (Or did you miss the space between the argument name and '
    'the ":" in the docstring?). Arguments in the docstring but not in the '
    'function signature: [arg3: Optional[Union[float, int, str]]].',
    'DOC105: Method `MyClass.func5`: Argument names match, but type hints do not '
    'match ',
    'DOC105: Method `MyClass.func6`: Argument names match, but type hints do not '
    'match ',
    'DOC101: Function `func72`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Function `func72`: Docstring arguments are different from function '
    'arguments. (Or did you miss the space between the argument name and the ":" '
    'in the docstring?). Arguments in the function signature but not in the '
    'docstring: [arg3: list, arg4: tuple, arg5: dict].',
]

expectedViolations_False_False = [
    'DOC101: Method `MyClass.func1_3`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func1_3`: Docstring arguments are different from '
    'function arguments. (Or did you miss the space between the argument name and '
    'the ":" in the docstring?). Arguments in the function signature but not in '
    'the docstring: [arg1: str, arg2: list[int]].',
    'DOC102: Method `MyClass.func1_6`: Docstring contains more arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func1_6`: Docstring arguments are different from '
    'function arguments. (Or did you miss the space between the argument name and '
    'the ":" in the docstring?). Arguments in the docstring but not in the '
    'function signature: [arg1: int].',
    'DOC101: Method `MyClass.func2`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func2`: Docstring arguments are different from '
    'function arguments. (Or did you miss the space between the argument name and '
    'the ":" in the docstring?). Arguments in the function signature but not in '
    'the docstring: [arg2: float | int | None].',
    'DOC102: Method `MyClass.func3`: Docstring contains more arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func3`: Docstring arguments are different from '
    'function arguments. (Or did you miss the space between the argument name and '
    'the ":" in the docstring?). Arguments in the docstring but not in the '
    'function signature: [arg3: Optional[Union[float, int, str]]].',
    'DOC101: Function `func72`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Function `func72`: Docstring arguments are different from function '
    'arguments. (Or did you miss the space between the argument name and the ":" '
    'in the docstring?). Arguments in the function signature but not in the '
    'docstring: [arg3: list, arg4: tuple, arg5: dict].',
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

    expectedViolationsCopy = copy.deepcopy(expectedViolations)
    if filename == 'function.py':
        _tweakViolationMsgForFunctions(expectedViolationsCopy)

    violations = _checkFile(
        filename=DATA_DIR / f'args/{filename}',
        checkTypeHint=optionDict['checkTypeHint'],
        checkArgOrder=optionDict['checkArgOrder'],
    )
    assert list(map(str, violations)) == expectedViolationsCopy


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
        'DOC201: Method `MyClass.func1_3` does not have a return section in '
        'docstring ',
        'DOC201: Method `MyClass.func1_5` does not have a return section in '
        'docstring ',
        'DOC201: Method `MyClass.func1_6` does not have a return section in '
        'docstring ',
        'DOC101: Method `MyClass.func2`: Docstring contains fewer arguments than in '
        'function signature. ',
        'DOC103: Method `MyClass.func2`: Docstring arguments are different from '
        'function arguments. (Or did you miss the space between the argument name and '
        'the ":" in the docstring?). Arguments in the function signature but not in '
        'the docstring: [arg2: float, arg3: str]. Arguments in the docstring but not '
        'in the function signature: [arg1: int].',
        'DOC201: Function `func52` does not have a return section in docstring ',
        'DOC202: Method `MyClass.func6` has a return section in docstring, but there '
        'are no return statements or annotations ',
        'DOC202: Method `MyClass.func7` has a return section in docstring, but there '
        'are no return statements or annotations ',
    ]

    expectedViolationsCopy = copy.deepcopy(expectedViolations)
    if filename == 'function.py':
        _tweakViolationMsgForFunctions(expectedViolationsCopy)

    assert list(map(str, violations)) == expectedViolationsCopy


def _tweakViolationMsgForFunctions(expectedViolationsCopy: List[str]) -> None:
    for i in range(len(expectedViolationsCopy)):
        expectedViolationsCopy[i] = expectedViolationsCopy[i].replace(
            'Method `MyClass.', 'Function `'
        )


expected_True = [
    'DOC101: Function `func3`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Function `func3`: Docstring arguments are different from function '
    'arguments. (Or did you miss the space between the argument name and the ":" '
    'in the docstring?). Arguments in the function signature but not in the '
    'docstring: [arg1: , arg2: , arg3: ]. Arguments in the docstring but not in '
    'the function signature: [var1: int, var2: str].',
    'DOC201: Function `func3` does not have a return section in docstring ',
]

expected_False = [
    'DOC101: Function `func1`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Function `func1`: Docstring arguments are different from function '
    'arguments. (Or did you miss the space between the argument name and the ":" '
    'in the docstring?). Arguments in the function signature but not in the '
    'docstring: [arg1: , arg2: , arg3: ].',
    'DOC201: Function `func1` does not have a return section in docstring ',
    'DOC101: Function `func2`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Function `func2`: Docstring arguments are different from function '
    'arguments. (Or did you miss the space between the argument name and the ":" '
    'in the docstring?). Arguments in the function signature but not in the '
    'docstring: [arg1: , arg2: , arg3: ].',
    'DOC201: Function `func2` does not have a return section in docstring ',
    'DOC101: Function `func3`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Function `func3`: Docstring arguments are different from function '
    'arguments. (Or did you miss the space between the argument name and the ":" '
    'in the docstring?). Arguments in the function signature but not in the '
    'docstring: [arg1: , arg2: , arg3: ]. Arguments in the docstring but not in '
    'the function signature: [var1: int, var2: str].',
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


def testInit():
    violations = _checkFile(filename=DATA_DIR / 'init/init.py')
    expected = [
        'DOC301: Class `A`: __init__() should not have a docstring; please combine it '
        'with the docstring of the class ',
        'DOC302: Class `B`: The docstring for the class does not need a "Returns" '
        'sections ',
        'DOC105: Method `C.__init__`: Argument names match, but type hints do not '
        'match ',
        'DOC302: Class `C`: The docstring for the class does not need a "Returns" '
        'sections ',
        'DOC103: Method `D.__init__`: Docstring arguments are different from function '
        'arguments. (Or did you miss the space between the argument name and the ":" '
        'in the docstring?). Arguments in the function signature but not in the '
        'docstring: [arg1: int, arg2: float]. Arguments in the docstring but not in '
        'the function signature: [var1: list, var2: dict].',
        'DOC302: Class `D`: The docstring for the class does not need a "Returns" '
        'sections ',
    ]
    assert list(map(str, violations)) == expected


def testYields():
    violations = _checkFile(filename=DATA_DIR / 'yields/cases.py')
    expected = [
        'DOC401: Method `A.method1` returns a Generator, but the docstring does not '
        'have a "Yields" section ',
        'DOC402: Method `A.method1` has "yield" statements, but the docstring does '
        'not have a "Yields" section ',
        'DOC402: Method `A.method2` has "yield" statements, but the docstring does '
        'not have a "Yields" section ',
        'DOC403: Method `A.method3` has a "Yields" section in the docstring, but '
        'there are no "yield" statements or a Generator return annotation ',
    ]
    assert list(map(str, violations)) == expected

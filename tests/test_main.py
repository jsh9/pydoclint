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
    'function arguments. (Or could be other formatting issues: '
    'https://github.com/jsh9/pydoclint/#notes-on-doc103). Arguments in the function signature but not in '
    'the docstring: [arg1: str, arg2: list[int]].',
    'DOC102: Method `MyClass.func1_6`: Docstring contains more arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func1_6`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://github.com/jsh9/pydoclint/#notes-on-doc103). Arguments in the docstring but not in the '
    'function signature: [arg1: int].',
    'DOC101: Method `MyClass.func2`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func2`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://github.com/jsh9/pydoclint/#notes-on-doc103). Arguments in the function signature but not in '
    'the docstring: [arg2: float | int | None].',
    'DOC102: Method `MyClass.func3`: Docstring contains more arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func3`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://github.com/jsh9/pydoclint/#notes-on-doc103). Arguments in the docstring but not in the '
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
    'arguments. (Or could be other formatting issues: '
    'https://github.com/jsh9/pydoclint/#notes-on-doc103). Arguments in the function signature but not in the '
    'docstring: [arg3: list, arg4: tuple, arg5: dict].',
]

expectedViolations_False_True = [
    'DOC101: Method `MyClass.func1_3`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func1_3`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://github.com/jsh9/pydoclint/#notes-on-doc103). Arguments in the function signature but not in '
    'the docstring: [arg1: str, arg2: list[int]].',
    'DOC102: Method `MyClass.func1_6`: Docstring contains more arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func1_6`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://github.com/jsh9/pydoclint/#notes-on-doc103). Arguments in the docstring but not in the '
    'function signature: [arg1: int].',
    'DOC101: Method `MyClass.func2`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func2`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://github.com/jsh9/pydoclint/#notes-on-doc103). Arguments in the function signature but not in '
    'the docstring: [arg2: float | int | None].',
    'DOC102: Method `MyClass.func3`: Docstring contains more arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func3`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://github.com/jsh9/pydoclint/#notes-on-doc103). Arguments in the docstring but not in the '
    'function signature: [arg3: Optional[Union[float, int, str]]].',
    'DOC104: Method `MyClass.func4`: Arguments are the same in the docstring and '
    'the function signature, but are in a different order. ',
    'DOC104: Method `MyClass.func6`: Arguments are the same in the docstring and '
    'the function signature, but are in a different order. ',
    'DOC101: Function `func72`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Function `func72`: Docstring arguments are different from function '
    'arguments. (Or could be other formatting issues: '
    'https://github.com/jsh9/pydoclint/#notes-on-doc103). Arguments in the function signature but not in the '
    'docstring: [arg3: list, arg4: tuple, arg5: dict].',
]

expectedViolations_True_False = [
    'DOC101: Method `MyClass.func1_3`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func1_3`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://github.com/jsh9/pydoclint/#notes-on-doc103). Arguments in the function signature but not in '
    'the docstring: [arg1: str, arg2: list[int]].',
    'DOC102: Method `MyClass.func1_6`: Docstring contains more arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func1_6`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://github.com/jsh9/pydoclint/#notes-on-doc103). Arguments in the docstring but not in the '
    'function signature: [arg1: int].',
    'DOC101: Method `MyClass.func2`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func2`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://github.com/jsh9/pydoclint/#notes-on-doc103). Arguments in the function signature but not in '
    'the docstring: [arg2: float | int | None].',
    'DOC102: Method `MyClass.func3`: Docstring contains more arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func3`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://github.com/jsh9/pydoclint/#notes-on-doc103). Arguments in the docstring but not in the '
    'function signature: [arg3: Optional[Union[float, int, str]]].',
    'DOC105: Method `MyClass.func5`: Argument names match, but type hints do not '
    'match ',
    'DOC105: Method `MyClass.func6`: Argument names match, but type hints do not '
    'match ',
    'DOC101: Function `func72`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Function `func72`: Docstring arguments are different from function '
    'arguments. (Or could be other formatting issues: '
    'https://github.com/jsh9/pydoclint/#notes-on-doc103). Arguments in the function signature but not in the '
    'docstring: [arg3: list, arg4: tuple, arg5: dict].',
]

expectedViolations_False_False = [
    'DOC101: Method `MyClass.func1_3`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func1_3`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://github.com/jsh9/pydoclint/#notes-on-doc103). Arguments in the function signature but not in '
    'the docstring: [arg1: str, arg2: list[int]].',
    'DOC102: Method `MyClass.func1_6`: Docstring contains more arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func1_6`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://github.com/jsh9/pydoclint/#notes-on-doc103). Arguments in the docstring but not in the '
    'function signature: [arg1: int].',
    'DOC101: Method `MyClass.func2`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func2`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://github.com/jsh9/pydoclint/#notes-on-doc103). Arguments in the function signature but not in '
    'the docstring: [arg2: float | int | None].',
    'DOC102: Method `MyClass.func3`: Docstring contains more arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func3`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://github.com/jsh9/pydoclint/#notes-on-doc103). Arguments in the docstring but not in the '
    'function signature: [arg3: Optional[Union[float, int, str]]].',
    'DOC101: Function `func72`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Function `func72`: Docstring arguments are different from function '
    'arguments. (Or could be other formatting issues: '
    'https://github.com/jsh9/pydoclint/#notes-on-doc103). Arguments in the function signature but not in the '
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
    'style, filename, option',
    list(
        itertools.product(
            ['numpy', 'google'],
            ['function.py', 'classmethod.py', 'method.py', 'staticmethod.py'],
            options,
        ),
    ),
)
def testArguments(
        style: str,
        filename: str,
        option: str,
) -> None:
    optionDict: Dict[str, bool] = optionDictLookup[option]
    expectedViolations: List[str] = expectedViolationsLookup[option]

    expectedViolationsCopy = copy.deepcopy(expectedViolations)
    if filename == 'function.py':
        _tweakViolationMsgForFunctions(expectedViolationsCopy)

    violations = _checkFile(
        filename=DATA_DIR / f'{style}/args/{filename}',
        checkTypeHint=optionDict['checkTypeHint'],
        checkArgOrder=optionDict['checkArgOrder'],
        style=style,
    )
    assert list(map(str, violations)) == expectedViolationsCopy


@pytest.mark.parametrize(
    'style, filename',
    list(
        itertools.product(
            ['numpy', 'google'],
            ['function.py', 'classmethod.py', 'method.py', 'staticmethod.py'],
        ),
    ),
)
def testReturns(style: str, filename: str) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/returns/{filename}',
        skipCheckingShortDocstrings=False,
        requireReturnSectionWhenReturningNone=True,
        style=style,
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
        'function arguments. (Or could be other formatting issues: '
        'https://github.com/jsh9/pydoclint/#notes-on-doc103). Arguments in the function signature but not in '
        'the docstring: [arg2: float, arg3: str]. Arguments in the docstring but not '
        'in the function signature: [arg1: int].',
        'DOC201: Function `func52` does not have a return section in docstring ',
        'DOC202: Method `MyClass.func6` has a return section in docstring, but there '
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
    'arguments. (Or could be other formatting issues: '
    'https://github.com/jsh9/pydoclint/#notes-on-doc103). Arguments in the function signature but not in the '
    'docstring: [arg1: , arg2: , arg3: ]. Arguments in the docstring but not in '
    'the function signature: [var1: int, var2: str].',
    'DOC201: Function `func3` does not have a return section in docstring ',
]

expected_False = [
    'DOC101: Function `func1`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Function `func1`: Docstring arguments are different from function '
    'arguments. (Or could be other formatting issues: '
    'https://github.com/jsh9/pydoclint/#notes-on-doc103). Arguments in the function signature but not in the '
    'docstring: [arg1: , arg2: , arg3: ].',
    'DOC201: Function `func1` does not have a return section in docstring ',
    'DOC101: Function `func2`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Function `func2`: Docstring arguments are different from function '
    'arguments. (Or could be other formatting issues: '
    'https://github.com/jsh9/pydoclint/#notes-on-doc103). Arguments in the function signature but not in the '
    'docstring: [arg1: , arg2: , arg3: ].',
    'DOC201: Function `func2` does not have a return section in docstring ',
    'DOC101: Function `func3`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Function `func3`: Docstring arguments are different from function '
    'arguments. (Or could be other formatting issues: '
    'https://github.com/jsh9/pydoclint/#notes-on-doc103). Arguments in the function signature but not in the '
    'docstring: [arg1: , arg2: , arg3: ]. Arguments in the docstring but not in '
    'the function signature: [var1: int, var2: str].',
    'DOC201: Function `func3` does not have a return section in docstring ',
]


@pytest.mark.parametrize(
    'style, skipCheckingShortDocstrings, expected',
    [
        ('numpy', True, expected_True),
        ('numpy', False, expected_False),
        ('google', True, expected_True),
        ('google', False, expected_False),
    ],
)
def testSkipCheckingShortDocstrings(
        style: str,
        skipCheckingShortDocstrings: bool,
        expected: List[str],
) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/short_docstrings/cases.py',
        skipCheckingShortDocstrings=skipCheckingShortDocstrings,
        style=style,
    )
    assert list(map(str, violations)) == expected


@pytest.mark.parametrize(
    'style',
    ['numpy', 'google'],
)
def testInit(style: str) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/init/init.py',
        style=style,
    )
    expected = [
        'DOC301: Class `A`: __init__() should not have a docstring; please combine it '
        'with the docstring of the class ',
        'DOC302: Class `B`: The class docstring does not need a "Returns" section, '
        'because __init__() cannot return anything ',
        'DOC105: Method `C.__init__`: Argument names match, but type hints do not '
        'match ',
        'DOC302: Class `C`: The class docstring does not need a "Returns" section, '
        'because __init__() cannot return anything ',
        'DOC103: Method `D.__init__`: Docstring arguments are different from function '
        'arguments. (Or could be other formatting issues: '
        'https://github.com/jsh9/pydoclint/#notes-on-doc103). Arguments in the function signature but not in the '
        'docstring: [arg1: int, arg2: float]. Arguments in the docstring but not in '
        'the function signature: [var1: list, var2: dict].',
        'DOC302: Class `D`: The class docstring does not need a "Returns" section, '
        'because __init__() cannot return anything ',
    ]
    assert list(map(str, violations)) == expected


@pytest.mark.parametrize(
    'style',
    ['numpy', 'google'],
)
def testAllowInitDocstring(style: str) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/allow_init_docstring/cases.py',
        style=style,
        allowInitDocstring=True,
    )
    expected = [
        'DOC304: Class `A`: Class docstring has an argument/parameter section; please '
        'put it in the __init__() docstring ',
        'DOC302: Class `B`: The class docstring does not need a "Returns" section, '
        'because __init__() cannot return anything ',
        'DOC303: Class `B`: The __init__() docstring does not need a "Returns" '
        'section, because it cannot return anything ',
        'DOC304: Class `B`: Class docstring has an argument/parameter section; please '
        'put it in the __init__() docstring ',
        'DOC302: Class `B`: The class docstring does not need a "Returns" section, '
        'because __init__() cannot return anything ',
        'DOC305: Class `C`: Class docstring has a "Raises" section; please put it in '
        'the __init__() docstring ',
        'DOC306: Class `D`: The class docstring does not need a "Yields" section, '
        'because __init__() cannot yield anything ',
        'DOC307: Class `D`: The __init__() docstring does not need a "Yields" '
        'section, because __init__() cannot yield anything ',
        'DOC306: Class `D`: The class docstring does not need a "Yields" section, '
        'because __init__() cannot yield anything ',
        'DOC403: Method `D.__init__` has a "Yields" section in the docstring, but '
        'there are no "yield" statements or a Generator return annotation ',
    ]
    assert list(map(str, violations)) == expected


@pytest.mark.parametrize('style', ['numpy', 'google'])
def testYields(style: str) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/yields/cases.py',
        style=style,
    )
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


@pytest.mark.parametrize(
    'style, skipRaisesCheck',
    itertools.product(
        ['numpy', 'google'],
        [False, True],
    ),
)
def testRaises(style: str, skipRaisesCheck: bool) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/raises/cases.py',
        skipCheckingRaises=skipRaisesCheck,
        style=style,
    )
    expected0 = [
        'DOC501: Method `B.func1` has "raise" statements, but the docstring does not '
        'have a "Raises" section ',
        'DOC502: Method `B.func5` has a "Raises" section in the docstring, but there '
        'are not "raise" statements in the body ',
        'DOC502: Method `B.func7` has a "Raises" section in the docstring, but there '
        'are not "raise" statements in the body ',
    ]
    expected1 = []
    expected = expected1 if skipRaisesCheck else expected0
    assert list(map(str, violations)) == expected


@pytest.mark.parametrize('style', ['numpy', 'google'])
def testStarsInArgumentList(style: str) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/star_args/cases.py',
        style=style,
    )
    expected = [
        'DOC103: Function `func2`: Docstring arguments are different from function '
        'arguments. (Or could be other formatting issues: '
        'https://github.com/jsh9/pydoclint/#notes-on-doc103). Arguments in the function signature but not in the '
        'docstring: [**kwargs: ]. Arguments in the docstring but not in the function '
        'signature: [kwargs: ].',
        'DOC103: Function `func4`: Docstring arguments are different from function '
        'arguments. (Or could be other formatting issues: '
        'https://github.com/jsh9/pydoclint/#notes-on-doc103). Arguments in the function signature but not in the '
        'docstring: [*args: ]. Arguments in the docstring but not in the function '
        'signature: [args: ].',
        'DOC101: Function `func6`: Docstring contains fewer arguments than in '
        'function signature. ',
        'DOC103: Function `func6`: Docstring arguments are different from function '
        'arguments. (Or could be other formatting issues: '
        'https://github.com/jsh9/pydoclint/#notes-on-doc103). Arguments in the function signature but not in the '
        'docstring: [**kwargs: , *args: ].',
        'DOC101: Function `func7`: Docstring contains fewer arguments than in '
        'function signature. ',
        'DOC103: Function `func7`: Docstring arguments are different from function '
        'arguments. (Or could be other formatting issues: '
        'https://github.com/jsh9/pydoclint/#notes-on-doc103). Arguments in the function signature but not in the '
        'docstring: [**kwargs: , *args: , arg1: float, arg2: str]. Arguments in the '
        'docstring but not in the function signature: [arg1: int, arg2: dict].',
    ]
    assert list(map(str, violations)) == expected


def testParsingErrors_google() -> None:
    violations = _checkFile(
        filename=DATA_DIR / 'google/parsing_errors/cases.py',
        style='google',
    )
    expected = [
        'DOC001: Function/method `__init__`: Potential formatting errors in '
        "docstring. Error message: Expected a colon in 'arg1'."
    ]
    assert list(map(str, violations)) == expected


def testParsingErrors_numpy() -> None:
    violations = _checkFile(
        filename=DATA_DIR / 'numpy/parsing_errors/cases.py',
        style='numpy',
    )
    expected = [
        'DOC001: Function/method `__init__`: Potential formatting errors in '
        'docstring. Error message: The section Parameters appears twice in  Some '
        'class  Parameters ----------     arg1     arg2  Parameters ----------     '
        'arg3     arg4'
    ]
    assert list(map(str, violations)) == expected


@pytest.mark.parametrize(
    'style, rrs',
    itertools.product(
        ['numpy', 'google'],
        [False, True],
    ),
)
def testNoReturnSection(
        style: str,
        rrs: bool,
) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/no_return_section/cases.py',
        style=style,
        requireReturnSectionWhenReturningNone=rrs,
    )
    expected_lookup = {
        True: [
            'DOC201: Function `func1` does not have a return section in docstring ',
            'DOC201: Function `func2` does not have a return section in docstring ',
            'DOC201: Function `func3` does not have a return section in docstring ',
            'DOC201: Function `func4` does not have a return section in docstring ',
            'DOC201: Function `func5` does not have a return section in docstring ',
        ],
        False: [
            'DOC201: Function `func2` does not have a return section in docstring ',
            'DOC201: Function `func3` does not have a return section in docstring ',
            'DOC201: Function `func4` does not have a return section in docstring ',
            'DOC201: Function `func5` does not have a return section in docstring ',
        ],
    }
    assert list(map(str, violations)) == expected_lookup[rrs]


@pytest.mark.parametrize(
    'style',
    ['numpy', 'google'],
)
def testPropertyMethod(style: str) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/property_method/cases.py',
        style=style,
        skipCheckingShortDocstrings=True,
    )
    expected = []
    assert list(map(str, violations)) == expected


def testPlayground() -> None:
    """
    This is a placeholder test for testing the `playground.py` file.

    When you want to quickly test something, you can add contents into
    tests/data/playground.py and run this test function.
    """
    violations = _checkFile(
        filename=DATA_DIR / 'playground.py',
        style='google',
    )
    expected = []
    assert list(map(str, violations)) == expected

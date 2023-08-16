import copy
import itertools
from pathlib import Path
from typing import Any, Dict, List

import pytest

from pydoclint.main import _checkFile

THIS_DIR = Path(__file__).parent
DATA_DIR = THIS_DIR / 'data'


expectedViolations_True = [
    'DOC101: Method `MyClass.func1_3`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC109: Method `MyClass.func1_3`: The option `--arg-type-hints-in-docstring` is `True` '
    'but there are no type hints in the docstring arg list ',
    'DOC103: Method `MyClass.func1_3`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the function signature but not in '
    'the docstring: [arg1: str, arg2: list[int]].',
    'DOC102: Method `MyClass.func1_6`: Docstring contains more arguments than in '
    'function signature. ',
    'DOC106: Method `MyClass.func1_6`: The option `--arg-type-hints-in-signature` is `True` '
    'but there are no argument type hints in the signature ',
    'DOC103: Method `MyClass.func1_6`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the docstring but not in the '
    'function signature: [arg1: int].',
    'DOC101: Method `MyClass.func2`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func2`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the function signature but not in '
    'the docstring: [arg2: float | int | None].',
    'DOC102: Method `MyClass.func3`: Docstring contains more arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func3`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the docstring but not in the '
    'function signature: [arg3: Optional[Union[float, int, str]]].',
    'DOC104: Method `MyClass.func4`: Arguments are the same in the docstring and '
    'the function signature, but are in a different order. ',
    'DOC105: Method `MyClass.func5`: Argument names match, but type hints do not match ',
    'DOC104: Method `MyClass.func6`: Arguments are the same in the docstring and '
    'the function signature, but are in a different order. ',
    'DOC105: Method `MyClass.func6`: Argument names match, but type hints do not match ',
    'DOC101: Function `func72`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC109: Function `func72`: The option `--arg-type-hints-in-docstring` is `True` '
    'but there are no type hints in the docstring arg list ',
    'DOC103: Function `func72`: Docstring arguments are different from function '
    'arguments. (Or could be other formatting issues: '
    'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the function signature but not in the '
    'docstring: [arg3: list, arg4: tuple, arg5: dict].',
]

expectedViolations_False = [
    'DOC101: Method `MyClass.func1_3`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC109: Method `MyClass.func1_3`: The option `--arg-type-hints-in-docstring` is `True` '
    'but there are no type hints in the docstring arg list ',
    'DOC103: Method `MyClass.func1_3`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the function signature but not in '
    'the docstring: [arg1: str, arg2: list[int]].',
    'DOC102: Method `MyClass.func1_6`: Docstring contains more arguments than in '
    'function signature. ',
    'DOC106: Method `MyClass.func1_6`: The option `--arg-type-hints-in-signature` is `True` '
    'but there are no argument type hints in the signature ',
    'DOC103: Method `MyClass.func1_6`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the docstring but not in the '
    'function signature: [arg1: int].',
    'DOC101: Method `MyClass.func2`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func2`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the function signature but not in '
    'the docstring: [arg2: float | int | None].',
    'DOC102: Method `MyClass.func3`: Docstring contains more arguments than in '
    'function signature. ',
    'DOC103: Method `MyClass.func3`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the docstring but not in the '
    'function signature: [arg3: Optional[Union[float, int, str]]].',
    'DOC105: Method `MyClass.func5`: Argument names match, but type hints do not '
    'match ',
    'DOC105: Method `MyClass.func6`: Argument names match, but type hints do not '
    'match ',
    'DOC101: Function `func72`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC109: Function `func72`: The option `--arg-type-hints-in-docstring` is `True` '
    'but there are no type hints in the docstring arg list ',
    'DOC103: Function `func72`: Docstring arguments are different from function '
    'arguments. (Or could be other formatting issues: '
    'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the function signature but not in the '
    'docstring: [arg3: list, arg4: tuple, arg5: dict].',
]

expectedViolationsLookup: Dict[bool, List[str]] = {
    True: expectedViolations_True,
    False: expectedViolations_False,
}


@pytest.mark.parametrize(
    'style, filename, checkArgOrder',
    list(
        itertools.product(
            ['numpy', 'google', 'sphinx'],
            ['function.py', 'classmethod.py', 'method.py', 'staticmethod.py'],
            [True, False],
        ),
    ),
)
def testArguments(
        style: str,
        filename: str,
        checkArgOrder: bool,
) -> None:
    expectedViolations: List[str] = expectedViolationsLookup[checkArgOrder]

    expectedViolationsCopy = copy.deepcopy(expectedViolations)
    if filename == 'function.py':
        _tweakViolationMsgForFunctions(expectedViolationsCopy)

    violations = _checkFile(
        filename=DATA_DIR / f'{style}/args/{filename}',
        checkArgOrder=checkArgOrder,
        checkReturnTypes=False,  # because this test only checks arguments
        style=style,
    )
    assert list(map(str, violations)) == expectedViolationsCopy


@pytest.mark.parametrize(
    'style, filename',
    list(
        itertools.product(
            ['numpy', 'google', 'sphinx'],
            ['function.py', 'classmethod.py', 'method.py', 'staticmethod.py'],
        ),
    ),
)
def testReturns(style: str, filename: str) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/returns/{filename}',
        skipCheckingShortDocstrings=True,
        requireReturnSectionWhenReturningNothing=True,
        style=style,
    )

    expectedViolations: List[str] = [
        'DOC201: Method `MyClass.func1_6` does not have a return section in '
        'docstring ',
        'DOC203: Method `MyClass.func1_6` return type(s) in docstring not consistent with '
        'the return annotation. Return annotation has 1 type(s); docstring '
        'return section has 0 type(s).',
        'DOC101: Method `MyClass.func2`: Docstring contains fewer arguments than in '
        'function signature. ',
        'DOC103: Method `MyClass.func2`: Docstring arguments are different from '
        'function arguments. (Or could be other formatting issues: '
        'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the function signature but not in '
        'the docstring: [arg2: float, arg3: str]. Arguments in the docstring but not '
        'in the function signature: [arg1: int].',
        'DOC203: Method `MyClass.func2` return type(s) in docstring not consistent with the '
        "return annotation. Return annotation types: ['int | list[float]']; docstring "
        "return section types: ['int']",
        'DOC203: Method `MyClass.func4` return type(s) in docstring not consistent with the '
        "return annotation. Return annotation types: ['int']; docstring return "
        "section types: ['float']",
        'DOC202: Method `MyClass.func6` has a return section in docstring, but there '
        'are no return statements or annotations ',
        'DOC203: Method `MyClass.func6` return type(s) in docstring not consistent with the '
        'return annotation. Return annotation has 0 type(s); docstring return section '
        'has 1 type(s).',
        'DOC203: Method `MyClass.func62` return type(s) in docstring not consistent with the '
        "return annotation. Return annotation types: ['float']; docstring return "
        "section types: ['int']",
        'DOC203: Method `MyClass.func7` return type(s) in docstring not consistent with the '
        'return annotation. Return annotation has 0 type(s); docstring return section '
        'has 1 type(s).',
    ]

    if style == 'google':
        expectedViolations.append(
            'DOC203: Method `MyClass.func82` return type(s) in docstring not consistent with '
            "the return annotation. Return annotation types: ['Tuple[int, bool]']; "
            "docstring return section types: ['int']"
        )

    if style == 'sphinx':
        expectedViolations.append(
            'DOC203: Method `MyClass.func82` return type(s) in docstring not consistent with '
            "the return annotation. Return annotation types: ['Tuple[int, bool]']; "
            "docstring return section types: ['bool']"
        )

    expectedViolations.extend([
        'DOC202: Method `MyClass.func101` has a return section in docstring, but '
        'there are no return statements or annotations ',
        'DOC203: Method `MyClass.func101` return type(s) in docstring not consistent '
        'with the return annotation. Return annotation has 0 type(s); docstring '
        'return section has 1 type(s).',
        'DOC201: Function `inner101` does not have a return section in docstring ',
        'DOC203: Function `inner101` return type(s) in docstring not consistent with '
        'the return annotation. Return annotation has 1 type(s); docstring return '
        'section has 0 type(s).',
    ])

    expectedViolationsCopy = copy.deepcopy(expectedViolations)
    if filename == 'function.py':
        _tweakViolationMsgForFunctions(expectedViolationsCopy)

    assert list(map(str, violations)) == expectedViolationsCopy


@pytest.mark.parametrize(
    'style, require',
    list(
        itertools.product(
            ['numpy', 'google', 'sphinx'],
            [True, False],
        ),
    ),
)
def testReturns_returningNone(style: str, require: bool) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/returning_none/cases.py',
        skipCheckingShortDocstrings=True,
        requireReturnSectionWhenReturningNothing=require,
        style=style,
    )
    expectedViolationsCopy = (
        [
            'DOC201: Function `func` does not have a return section in docstring ',
            'DOC203: Function `func` return type(s) in docstring not consistent with the '
            'return annotation. Return annotation has 1 type(s); docstring return section '
            'has 0 type(s).',
        ]
        if require
        else []
    )
    assert list(map(str, violations)) == expectedViolationsCopy


@pytest.mark.parametrize(
    'style, require',
    list(
        itertools.product(
            ['numpy', 'google', 'sphinx'],
            [True, False],
        ),
    ),
)
def testReturns_returningNoReturn(style: str, require: bool) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/returning_noreturn/cases.py',
        skipCheckingShortDocstrings=True,
        requireReturnSectionWhenReturningNothing=require,
        style=style,
    )
    expectedViolationsCopy = (
        [
            'DOC201: Function `func` does not have a return section in docstring ',
            'DOC203: Function `func` return type(s) in docstring not consistent with the '
            'return annotation. Return annotation has 1 type(s); docstring return section '
            'has 0 type(s).',
        ]
        if require
        else []
    )
    assert list(map(str, violations)) == expectedViolationsCopy


def _tweakViolationMsgForFunctions(expectedViolationsCopy: List[str]) -> None:
    for i in range(len(expectedViolationsCopy)):
        expectedViolationsCopy[i] = expectedViolationsCopy[i].replace(
            'Method `MyClass.', 'Function `'
        )


expected_skipCheckingShortDocstrings_True = [
    'DOC101: Function `func3`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC106: Function `func3`: The option `--arg-type-hints-in-signature` is `True` '
    'but there are no argument type hints in the signature ',
    'DOC107: Function `func3`: The option `--arg-type-hints-in-signature` is `True` '
    'but not all args in the signature have type hints ',
    'DOC103: Function `func3`: Docstring arguments are different from function '
    'arguments. (Or could be other formatting issues: '
    'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the function signature but not in the '
    'docstring: [arg1: , arg2: , arg3: ]. Arguments in the docstring but not in '
    'the function signature: [var1: int, var2: str].',
]

expected_skipCheckingShortDocstrings_False = [
    'DOC101: Function `func1`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC106: Function `func1`: The option `--arg-type-hints-in-signature` is `True` '
    'but there are no argument type hints in the signature ',
    'DOC107: Function `func1`: The option `--arg-type-hints-in-signature` is `True` '
    'but not all args in the signature have type hints ',
    'DOC109: Function `func1`: The option `--arg-type-hints-in-docstring` is `True` '
    'but there are no type hints in the docstring arg list ',
    'DOC103: Function `func1`: Docstring arguments are different from function '
    'arguments. (Or could be other formatting issues: '
    'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the '
    'function signature but not in the docstring: [arg1: , arg2: , arg3: ].',
    'DOC201: Function `func1` does not have a return section in docstring ',
    'DOC203: Function `func1` return type(s) in docstring not consistent with the '
    'return annotation. Return annotation has 1 type(s); docstring return section '
    'has 0 type(s).',
    'DOC101: Function `func2`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC106: Function `func2`: The option `--arg-type-hints-in-signature` is `True` '
    'but there are no argument type hints in the signature ',
    'DOC107: Function `func2`: The option `--arg-type-hints-in-signature` is `True` '
    'but not all args in the signature have type hints ',
    'DOC109: Function `func2`: The option `--arg-type-hints-in-docstring` is `True` '
    'but there are no type hints in the docstring arg list ',
    'DOC103: Function `func2`: Docstring arguments are different from function '
    'arguments. (Or could be other formatting issues: '
    'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the '
    'function signature but not in the docstring: [arg1: , arg2: , arg3: ].',
    'DOC201: Function `func2` does not have a return section in docstring ',
    'DOC203: Function `func2` return type(s) in docstring not consistent with the '
    'return annotation. Return annotation has 1 type(s); docstring return section '
    'has 0 type(s).',
    'DOC101: Function `func3`: Docstring contains fewer arguments than in '
    'function signature. ',
    'DOC106: Function `func3`: The option `--arg-type-hints-in-signature` is `True` '
    'but there are no argument type hints in the signature ',
    'DOC107: Function `func3`: The option `--arg-type-hints-in-signature` is `True` '
    'but not all args in the signature have type hints ',
    'DOC103: Function `func3`: Docstring arguments are different from function '
    'arguments. (Or could be other formatting issues: '
    'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the '
    'function signature but not in the docstring: [arg1: , arg2: , arg3: ]. '
    'Arguments in the docstring but not in the function signature: [var1: int, '
    'var2: str].',
]


@pytest.mark.parametrize(
    'style, skipCheckingShortDocstrings, expected',
    [
        ('numpy', True, expected_skipCheckingShortDocstrings_True),
        ('numpy', False, expected_skipCheckingShortDocstrings_False),
        ('google', True, expected_skipCheckingShortDocstrings_True),
        ('google', False, expected_skipCheckingShortDocstrings_False),
        ('sphinx', True, expected_skipCheckingShortDocstrings_True),
        ('sphinx', False, expected_skipCheckingShortDocstrings_False),
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
        checkReturnTypes=True,
        style=style,
    )
    assert list(map(str, violations)) == expected


@pytest.mark.parametrize(
    'style',
    ['numpy', 'google', 'sphinx'],
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
        'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the function signature but not in the '
        'docstring: [arg1: int, arg2: float]. Arguments in the docstring but not in '
        'the function signature: [var1: list, var2: dict].',
        'DOC302: Class `D`: The class docstring does not need a "Returns" section, '
        'because __init__() cannot return anything ',
    ]
    assert list(map(str, violations)) == expected


@pytest.mark.parametrize(
    'style',
    ['numpy', 'google', 'sphinx'],
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


@pytest.mark.parametrize('style', ['numpy', 'google', 'sphinx'])
def testYields(style: str) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/yields/cases.py',
        checkReturnTypes=False,
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
        'DOC401: Method `A.method6` returns a Generator, but the docstring does not '
        'have a "Yields" section ',
        'DOC402: Method `A.method6` has "yield" statements, but the docstring does '
        'not have a "Yields" section ',
        'DOC402: Method `A.method8a` has "yield" statements, but the docstring does '
        'not have a "Yields" section ',
        'DOC402: Method `A.method8b` has "yield" statements, but the docstring does '
        'not have a "Yields" section ',
        'DOC402: Method `A.method8c` has "yield" statements, but the docstring does '
        'not have a "Yields" section ',
        'DOC402: Method `A.method8d` has "yield" statements, but the docstring does '
        'not have a "Yields" section ',
        'DOC201: Method `A.zipLists2` does not have a return section in docstring ',
        'DOC403: Method `A.zipLists2` has a "Yields" section in the docstring, but '
        'there are no "yield" statements or a Generator return annotation ',
        'DOC402: Function `inner9b` has "yield" statements, but the docstring does '
        'not have a "Yields" section ',
        'DOC201: Method `A.method9c` does not have a return section in docstring ',
        'DOC403: Method `A.method9c` has a "Yields" section in the docstring, but '
        'there are no "yield" statements or a Generator return annotation ',
        'DOC402: Method `A.method9d` has "yield" statements, but the docstring does '
        'not have a "Yields" section ',
        'DOC402: Function `inner9d` has "yield" statements, but the docstring does '
        'not have a "Yields" section ',
    ]
    assert list(map(str, violations)) == expected


@pytest.mark.parametrize(
    'style, skipRaisesCheck',
    itertools.product(
        ['numpy', 'google', 'sphinx'],
        [False, True],
    ),
)
def testRaises(style: str, skipRaisesCheck: bool) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/raises/cases.py',
        skipCheckingRaises=skipRaisesCheck,
        argTypeHintsInSignature=False,
        argTypeHintsInDocstring=False,
        checkReturnTypes=False,
        style=style,
    )
    expected0 = [
        'DOC501: Method `B.func1` has "raise" statements, but the docstring does not '
        'have a "Raises" section ',
        'DOC502: Method `B.func5` has a "Raises" section in the docstring, but there '
        'are not "raise" statements in the body ',
        'DOC502: Method `B.func7` has a "Raises" section in the docstring, but there '
        'are not "raise" statements in the body ',
        'DOC502: Method `B.func9a` has a "Raises" section in the docstring, but there '
        'are not "raise" statements in the body ',
        'DOC501: Function `inner9a` has "raise" statements, but the docstring does '
        'not have a "Raises" section ',
    ]
    expected1 = []
    expected = expected1 if skipRaisesCheck else expected0
    assert list(map(str, violations)) == expected


@pytest.mark.parametrize('style', ['numpy', 'google', 'sphinx'])
def testStarsInArgumentList(style: str) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/star_args/cases.py',
        style=style,
    )
    expected = [
        'DOC110: Function `func2`: The option `--arg-type-hints-in-docstring` is `True` '
        'but not all args in the docstring arg list have type hints ',
        'DOC103: Function `func2`: Docstring arguments are different from function '
        'arguments. (Or could be other formatting issues: '
        'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the function signature but not in the '
        'docstring: [**kwargs: ]. Arguments in the docstring but not in the function '
        'signature: [kwargs: ].',
        'DOC110: Function `func4`: The option `--arg-type-hints-in-docstring` is `True` '
        'but not all args in the docstring arg list have type hints ',
        'DOC103: Function `func4`: Docstring arguments are different from function '
        'arguments. (Or could be other formatting issues: '
        'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the function signature but not in the '
        'docstring: [*args: ]. Arguments in the docstring but not in the function '
        'signature: [args: ].',
        'DOC101: Function `func6`: Docstring contains fewer arguments than in '
        'function signature. ',
        'DOC103: Function `func6`: Docstring arguments are different from function '
        'arguments. (Or could be other formatting issues: '
        'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the function signature but not in the '
        'docstring: [**kwargs: , *args: ].',
        'DOC101: Function `func7`: Docstring contains fewer arguments than in '
        'function signature. ',
        'DOC103: Function `func7`: Docstring arguments are different from function '
        'arguments. (Or could be other formatting issues: '
        'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the function signature but not in the '
        'docstring: [**kwargs: , *args: , arg1: float, arg2: str]. Arguments in the '
        'docstring but not in the function signature: [arg1: int, arg2: dict].',
    ]
    assert list(map(str, violations)) == expected


@pytest.mark.parametrize('style', ['numpy', 'google', 'sphinx'])
def testStarsInArgumentList2(style: str) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/star_args/cases2.py',
        argTypeHintsInSignature=True,
        argTypeHintsInDocstring=False,
        allowInitDocstring=True,
        style=style,
    )
    expected = []
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


def testParsingErrors_sphinx() -> None:
    violations = _checkFile(
        filename=DATA_DIR / 'sphinx/parsing_errors/cases.py',
        style='sphinx',
    )
    expected = []  # not sure how to craft docstrings with parsing errors yet
    assert list(map(str, violations)) == expected


def testParsingErrors_numpy() -> None:
    violations = _checkFile(
        filename=DATA_DIR / 'numpy/parsing_errors/cases.py',
        argTypeHintsInDocstring=False,
        argTypeHintsInSignature=False,
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
        ['numpy', 'google', 'sphinx'],
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
        checkReturnTypes=False,
        requireReturnSectionWhenReturningNothing=rrs,
    )
    expected_lookup = {
        True: [
            'DOC201: Function `func1` does not have a return section in docstring ',
            'DOC201: Function `func2` does not have a return section in docstring ',
            'DOC201: Function `func3` does not have a return section in docstring ',
            'DOC201: Function `func4` does not have a return section in docstring ',
            'DOC201: Function `func5` does not have a return section in docstring ',
            'DOC201: Function `func7` does not have a return section in docstring ',
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
    ['numpy', 'google', 'sphinx'],
)
def testPropertyMethod(style: str) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/property_method/cases.py',
        style=style,
        skipCheckingShortDocstrings=True,
    )
    expected = []
    assert list(map(str, violations)) == expected


@pytest.mark.parametrize(
    'style, checkReturnTypes',
    itertools.product(
        ['numpy', 'google', 'sphinx'],
        [False, True],
    ),
)
def testAbstractMethod(style: str, checkReturnTypes: bool) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/abstract_method/cases.py',
        checkReturnTypes=checkReturnTypes,
        style=style,
    )
    if checkReturnTypes:
        expected = [
            'DOC201: Method `AbstractClass.another_abstract_method` does not have a '
            'return section in docstring ',
            'DOC203: Method `AbstractClass.another_abstract_method` return type(s) in '
            'docstring not consistent with the return annotation. Return annotation has 1 '
            'type(s); docstring return section has 0 type(s).',
            'DOC201: Method `AbstractClass.third_abstract_method` does not have a return '
            'section in docstring ',
            'DOC203: Method `AbstractClass.third_abstract_method` return type(s) in '
            'docstring not consistent with the return annotation. Return annotation has 1 '
            'type(s); docstring return section has 0 type(s).',
        ]
    else:
        expected = [
            'DOC201: Method `AbstractClass.another_abstract_method` does not have a '
            'return section in docstring ',
            'DOC201: Method `AbstractClass.third_abstract_method` does not have a return '
            'section in docstring ',
        ]

    assert list(map(str, violations)) == expected


@pytest.mark.parametrize(
    'style, argTypeHintsInDocstring, argTypeHintsInSignature',
    itertools.product(
        ['numpy', 'google', 'sphinx'],
        [False, True],
        [False, True],
    ),
)
def testTypeHintChecking(
        style: str,
        argTypeHintsInDocstring: bool,
        argTypeHintsInSignature: bool,
) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/type_hints/cases.py',
        style=style,
        argTypeHintsInDocstring=argTypeHintsInDocstring,
        argTypeHintsInSignature=argTypeHintsInSignature,
    )

    expected_lookup = {
        (False, False): [
            'DOC108: Method `MyClass.func2`: The option `--arg-type-hints-in-signature` is '
            '`False` but there are argument type hints in the signature ',
            'DOC111: Method `MyClass.func3`: The option `--arg-type-hints-in-docstring` is '
            '`False` but there are type hints in the docstring arg list ',
            'DOC108: Method `MyClass.func4`: The option `--arg-type-hints-in-signature` is '
            '`False` but there are argument type hints in the signature ',
            'DOC111: Method `MyClass.func4`: The option `--arg-type-hints-in-docstring` is '
            '`False` but there are type hints in the docstring arg list ',
            'DOC108: Method `MyClass.func5`: The option `--arg-type-hints-in-signature` is '
            '`False` but there are argument type hints in the signature ',
            'DOC111: Method `MyClass.func5`: The option `--arg-type-hints-in-docstring` is '
            '`False` but there are type hints in the docstring arg list ',
            'DOC108: Method `MyClass.func6`: The option `--arg-type-hints-in-signature` is '
            '`False` but there are argument type hints in the signature ',
            'DOC111: Method `MyClass.func6`: The option `--arg-type-hints-in-docstring` is '
            '`False` but there are type hints in the docstring arg list ',
            'DOC108: Method `MyClass.func7`: The option `--arg-type-hints-in-signature` is '
            '`False` but there are argument type hints in the signature ',
            'DOC111: Method `MyClass.func7`: The option `--arg-type-hints-in-docstring` is '
            '`False` but there are type hints in the docstring arg list ',
        ],
        (False, True): [
            'DOC106: Method `MyClass.func1`: The option `--arg-type-hints-in-signature` is '
            '`True` but there are no argument type hints in the signature ',
            'DOC107: Method `MyClass.func1`: The option `--arg-type-hints-in-signature` is '
            '`True` but not all args in the signature have type hints ',
            'DOC106: Method `MyClass.func3`: The option `--arg-type-hints-in-signature` is '
            '`True` but there are no argument type hints in the signature ',
            'DOC107: Method `MyClass.func3`: The option `--arg-type-hints-in-signature` is '
            '`True` but not all args in the signature have type hints ',
            'DOC111: Method `MyClass.func3`: The option `--arg-type-hints-in-docstring` is '
            '`False` but there are type hints in the docstring arg list ',
            'DOC111: Method `MyClass.func4`: The option `--arg-type-hints-in-docstring` is '
            '`False` but there are type hints in the docstring arg list ',
            'DOC107: Method `MyClass.func5`: The option `--arg-type-hints-in-signature` is '
            '`True` but not all args in the signature have type hints ',
            'DOC111: Method `MyClass.func5`: The option `--arg-type-hints-in-docstring` is '
            '`False` but there are type hints in the docstring arg list ',
            'DOC111: Method `MyClass.func6`: The option `--arg-type-hints-in-docstring` is '
            '`False` but there are type hints in the docstring arg list ',
            'DOC107: Method `MyClass.func7`: The option `--arg-type-hints-in-signature` is '
            '`True` but not all args in the signature have type hints ',
            'DOC111: Method `MyClass.func7`: The option `--arg-type-hints-in-docstring` is '
            '`False` but there are type hints in the docstring arg list ',
        ],
        (True, False): [
            'DOC109: Method `MyClass.func1`: The option `--arg-type-hints-in-docstring` is '
            '`True` but there are no type hints in the docstring arg list ',
            'DOC110: Method `MyClass.func1`: The option `--arg-type-hints-in-docstring` is '
            '`True` but not all args in the docstring arg list have type hints ',
            'DOC108: Method `MyClass.func2`: The option `--arg-type-hints-in-signature` is '
            '`False` but there are argument type hints in the signature ',
            'DOC109: Method `MyClass.func2`: The option `--arg-type-hints-in-docstring` is '
            '`True` but there are no type hints in the docstring arg list ',
            'DOC110: Method `MyClass.func2`: The option `--arg-type-hints-in-docstring` is '
            '`True` but not all args in the docstring arg list have type hints ',
            'DOC108: Method `MyClass.func4`: The option `--arg-type-hints-in-signature` is '
            '`False` but there are argument type hints in the signature ',
            'DOC108: Method `MyClass.func5`: The option `--arg-type-hints-in-signature` is '
            '`False` but there are argument type hints in the signature ',
            'DOC110: Method `MyClass.func5`: The option `--arg-type-hints-in-docstring` is '
            '`True` but not all args in the docstring arg list have type hints ',
            'DOC108: Method `MyClass.func6`: The option `--arg-type-hints-in-signature` is '
            '`False` but there are argument type hints in the signature ',
            'DOC108: Method `MyClass.func7`: The option `--arg-type-hints-in-signature` is '
            '`False` but there are argument type hints in the signature ',
            'DOC110: Method `MyClass.func7`: The option `--arg-type-hints-in-docstring` is '
            '`True` but not all args in the docstring arg list have type hints ',
        ],
        (True, True): [
            'DOC106: Method `MyClass.func1`: The option `--arg-type-hints-in-signature` is '
            '`True` but there are no argument type hints in the signature ',
            'DOC107: Method `MyClass.func1`: The option `--arg-type-hints-in-signature` is '
            '`True` but not all args in the signature have type hints ',
            'DOC109: Method `MyClass.func1`: The option `--arg-type-hints-in-docstring` is '
            '`True` but there are no type hints in the docstring arg list ',
            'DOC110: Method `MyClass.func1`: The option `--arg-type-hints-in-docstring` is '
            '`True` but not all args in the docstring arg list have type hints ',
            'DOC109: Method `MyClass.func2`: The option `--arg-type-hints-in-docstring` is '
            '`True` but there are no type hints in the docstring arg list ',
            'DOC110: Method `MyClass.func2`: The option `--arg-type-hints-in-docstring` is '
            '`True` but not all args in the docstring arg list have type hints ',
            'DOC105: Method `MyClass.func2`: Argument names match, but type hints do not '
            'match ',
            'DOC106: Method `MyClass.func3`: The option `--arg-type-hints-in-signature` is '
            '`True` but there are no argument type hints in the signature ',
            'DOC107: Method `MyClass.func3`: The option `--arg-type-hints-in-signature` is '
            '`True` but not all args in the signature have type hints ',
            'DOC105: Method `MyClass.func3`: Argument names match, but type hints do not '
            'match ',
            'DOC107: Method `MyClass.func5`: The option `--arg-type-hints-in-signature` is '
            '`True` but not all args in the signature have type hints ',
            'DOC110: Method `MyClass.func5`: The option `--arg-type-hints-in-docstring` is '
            '`True` but not all args in the docstring arg list have type hints ',
            'DOC105: Method `MyClass.func5`: Argument names match, but type hints do not '
            'match ',
            'DOC105: Method `MyClass.func6`: Argument names match, but type hints do not '
            'match ',
            'DOC107: Method `MyClass.func7`: The option `--arg-type-hints-in-signature` is '
            '`True` but not all args in the signature have type hints ',
            'DOC110: Method `MyClass.func7`: The option `--arg-type-hints-in-docstring` is '
            '`True` but not all args in the docstring arg list have type hints ',
        ],
    }

    expected = expected_lookup[
        (argTypeHintsInDocstring, argTypeHintsInSignature)
    ]
    assert list(map(str, violations)) == expected


def testNonAscii() -> None:
    """Don't crash on non ASCII arguments."""
    violations = _checkFile(
        filename=DATA_DIR / 'common/non_ascii/non_ascii.py',
        style='numpy',
        skipCheckingShortDocstrings=False,
    )
    expected = []
    assert list(map(str, violations)) == expected


@pytest.mark.parametrize(
    'filename, options, expectedViolations',
    [
        ('edge_case_01.py', {'style': 'sphinx'}, []),
        (
            'edge_case_02_syntax_error_in_type_hints.py',
            {'style': 'numpy'},
            [
                'DOC106: Function `func1`: The option `--arg-type-hints-in-signature` is '
                '`True` but there are no argument type hints in the signature ',
                'DOC107: Function `func1`: The option `--arg-type-hints-in-signature` is '
                '`True` but not all args in the signature have type hints ',
                'DOC105: Function `func1`: Argument names match, but type hints do not match ',
                'DOC106: Function `func2`: The option `--arg-type-hints-in-signature` is '
                '`True` but there are no argument type hints in the signature ',
                'DOC107: Function `func2`: The option `--arg-type-hints-in-signature` is '
                '`True` but not all args in the signature have type hints ',
                'DOC105: Function `func2`: Argument names match, but type hints do not match ',
                'DOC106: Function `func3`: The option `--arg-type-hints-in-signature` is '
                '`True` but there are no argument type hints in the signature ',
                'DOC107: Function `func3`: The option `--arg-type-hints-in-signature` is '
                '`True` but not all args in the signature have type hints ',
                'DOC105: Function `func3`: Argument names match, but type hints do not match ',
            ],
        ),
    ],
)
def testEdgeCases(
        filename: str,
        options: Dict[str, Any],
        expectedViolations: List[str],
) -> None:
    violations = _checkFile(
        filename=DATA_DIR / 'edge_cases' / filename,
        **options,
    )
    assert list(map(str, violations)) == expectedViolations


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

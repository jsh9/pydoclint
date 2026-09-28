import copy
import sys
from pathlib import Path

import pytest

from pydoclint.main import _checkFile

THIS_DIR = Path(__file__).parent
DATA_DIR = THIS_DIR / 'test_data'
ALL_STYLES: list[str] = ['google', 'numpy', 'sphinx']


def pythonVersionBelow310() -> bool:
    return sys.version_info < (3, 10)


expectedViolations_True = [
    'DOC101: Method `MyClass.func1_3`: Docstring contains fewer arguments than in '
    'function signature.',
    'DOC103: Method `MyClass.func1_3`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the function signature but not in '
    'the docstring: [arg1: str, arg2: list[int]].',
    'DOC102: Method `MyClass.func1_6`: Docstring contains more arguments than in '
    'function signature.',
    'DOC106: Method `MyClass.func1_6`: The option `--arg-type-hints-in-signature` is `True` '
    'but there are no argument type hints in the signature',
    'DOC103: Method `MyClass.func1_6`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the docstring but not in the '
    'function signature: [arg1: int].',
    'DOC101: Method `MyClass.func2`: Docstring contains fewer arguments than in '
    'function signature.',
    'DOC103: Method `MyClass.func2`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the function signature but not in '
    'the docstring: [arg2: float | int | None].',
    'DOC102: Method `MyClass.func3`: Docstring contains more arguments than in '
    'function signature.',
    'DOC103: Method `MyClass.func3`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the docstring but not in the '
    'function signature: [arg3: Optional[Union[float, int, str]]].',
    'DOC104: Method `MyClass.func4`: Arguments are the same in the docstring and '
    'the function signature, but are in a different order.',
    'DOC105: Method `MyClass.func5`: Argument names match, but type hints in these args '
    'do not match: arg1, arg2',
    'DOC104: Method `MyClass.func6`: Arguments are the same in the docstring and '
    'the function signature, but are in a different order.',
    'DOC105: Method `MyClass.func6`: Argument names match, but type hints in these args '
    'do not match: arg1, arg2',
    'DOC101: Function `func72`: Docstring contains fewer arguments than in '
    'function signature.',
    'DOC103: Function `func72`: Docstring arguments are different from function '
    'arguments. (Or could be other formatting issues: '
    'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the function signature but not in the '
    'docstring: [arg3: list, arg4: tuple, arg5: dict].',
]

expectedViolations_False = [
    'DOC101: Method `MyClass.func1_3`: Docstring contains fewer arguments than in '
    'function signature.',
    'DOC103: Method `MyClass.func1_3`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the function signature but not in '
    'the docstring: [arg1: str, arg2: list[int]].',
    'DOC102: Method `MyClass.func1_6`: Docstring contains more arguments than in '
    'function signature.',
    'DOC106: Method `MyClass.func1_6`: The option `--arg-type-hints-in-signature` is `True` '
    'but there are no argument type hints in the signature',
    'DOC103: Method `MyClass.func1_6`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the docstring but not in the '
    'function signature: [arg1: int].',
    'DOC101: Method `MyClass.func2`: Docstring contains fewer arguments than in '
    'function signature.',
    'DOC103: Method `MyClass.func2`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the function signature but not in '
    'the docstring: [arg2: float | int | None].',
    'DOC102: Method `MyClass.func3`: Docstring contains more arguments than in '
    'function signature.',
    'DOC103: Method `MyClass.func3`: Docstring arguments are different from '
    'function arguments. (Or could be other formatting issues: '
    'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the docstring but not in the '
    'function signature: [arg3: Optional[Union[float, int, str]]].',
    'DOC105: Method `MyClass.func5`: Argument names match, but type hints in '
    'these args do not match: arg1, arg2',
    'DOC105: Method `MyClass.func6`: Argument names match, but type hints in '
    'these args do not match: arg1, arg2',
    'DOC101: Function `func72`: Docstring contains fewer arguments than in '
    'function signature.',
    'DOC103: Function `func72`: Docstring arguments are different from function '
    'arguments. (Or could be other formatting issues: '
    'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the function signature but not in the '
    'docstring: [arg3: list, arg4: tuple, arg5: dict].',
]

expectedViolationsLookup: dict[bool, list[str]] = {
    True: expectedViolations_True,
    False: expectedViolations_False,
}


@pytest.mark.parametrize('checkArgOrder', [False, True])
@pytest.mark.parametrize(
    'filename',
    ['function.py', 'classmethod.py', 'method.py', 'staticmethod.py'],
)
@pytest.mark.parametrize('style', ALL_STYLES)
def testArguments(
        style: str,
        filename: str,
        checkArgOrder: bool,
) -> None:
    expectedViolations: list[str] = expectedViolationsLookup[checkArgOrder]

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


@pytest.mark.parametrize('checkClassAttr', [False, True])
@pytest.mark.parametrize('style', ALL_STYLES)
def testClassAttributes(
        style: str,
        checkClassAttr: bool,
) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/class_attributes/cases.py',
        checkClassAttributes=checkClassAttr,
        style=style,
    )

    expectedViolations: dict[bool, list[str]] = {
        True: [
            'DOC601: Class `MyClass1`: Class docstring contains fewer class attributes '
            'than actual class attributes.  (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
            'DOC603: Class `MyClass1`: Class docstring attributes are different from '
            'actual class attributes. (Or could be other formatting issues: '
            'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
            'Attributes in the class definition but not in the docstring: [hello: int, '
            'index: pd.DataFrame, world: dict]. Arguments in the docstring but not in the '
            'actual class attributes: [indices: pd.DataFrame]. (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
            'DOC105: Method `MyClass1.__init__`: Argument names match, but type hints in '
            'these args do not match: arg1',
            'DOC105: Method `MyClass1.do_something`: Argument names match, but type hints '
            'in these args do not match: arg2',
            'DOC601: Class `MyClass2`: Class docstring contains fewer class attributes '
            'than actual class attributes.  (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
            'DOC603: Class `MyClass2`: Class docstring attributes are different from '
            'actual class attributes. (Or could be other formatting issues: '
            'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
            'Attributes in the class definition but not in the docstring: [hello: int, '
            'index: int, world: dict]. Arguments in the docstring but not in the actual '
            'class attributes: [arg1: float, indices: int]. (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
            'DOC101: Method `MyClass2.__init__`: Docstring contains fewer arguments than '
            'in function signature.',
            'DOC103: Method `MyClass2.__init__`: Docstring arguments are different from '
            'function arguments. (Or could be other formatting issues: '
            'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
            'Arguments in the function signature but not in the docstring: [arg1: int].',
            'DOC105: Method `MyClass2.do_something`: Argument names match, but type hints '
            'in these args do not match: arg2',
            'DOC601: Class `MyClass3`: Class docstring contains fewer class attributes '
            'than actual class attributes.  (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
            'DOC603: Class `MyClass3`: Class docstring attributes are different from '
            'actual class attributes. (Or could be other formatting issues: '
            'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
            'Attributes in the class definition but not in the docstring: [hello: int, '
            'index: int, name: str, world: dict]. (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
            'DOC102: Method `MyClass3.__init__`: Docstring contains more arguments than '
            'in function signature.',
            'DOC103: Method `MyClass3.__init__`: Docstring arguments are different from '
            'function arguments. (Or could be other formatting issues: '
            'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
            'Arguments in the docstring but not in the function signature: [indices: int, '
            'name: str].',
            'DOC105: Method `MyClass3.do_something`: Argument names match, but type hints '
            'in these args do not match: arg2',
            'DOC602: Class `MyClass4`: Class docstring contains more class attributes '
            'than in actual class attributes.  (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
            'DOC603: Class `MyClass4`: Class docstring attributes are different from '
            'actual class attributes. (Or could be other formatting issues: '
            'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
            'Arguments in the docstring but not in the actual class attributes: [name: '
            'str]. (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
            'DOC605: Class `MyClass8`: Attribute names match, but type hints in these '
            'attributes do not match: arg2  (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
            'DOC604: Class `MyClass9`: Attributes are the same in docstring and class '
            'def, but are in a different order.  (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
        ],
        False: [
            'DOC105: Method `MyClass1.__init__`: Argument names match, but type hints in '
            'these args do not match: arg1',
            'DOC105: Method `MyClass1.do_something`: Argument names match, but type hints '
            'in these args do not match: arg2',
            'DOC101: Method `MyClass2.__init__`: Docstring contains fewer arguments than '
            'in function signature.',
            'DOC103: Method `MyClass2.__init__`: Docstring arguments are different from '
            'function arguments. (Or could be other formatting issues: '
            'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
            'Arguments in the function signature but not in the docstring: [arg1: int].',
            'DOC105: Method `MyClass2.do_something`: Argument names match, but type hints '
            'in these args do not match: arg2',
            'DOC102: Method `MyClass3.__init__`: Docstring contains more arguments than '
            'in function signature.',
            'DOC103: Method `MyClass3.__init__`: Docstring arguments are different from '
            'function arguments. (Or could be other formatting issues: '
            'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
            'Arguments in the docstring but not in the function signature: [indices: int, '
            'name: str].',
            'DOC105: Method `MyClass3.do_something`: Argument names match, but type hints '
            'in these args do not match: arg2',
        ],
    }

    assert list(map(str, violations)) == expectedViolations[checkClassAttr]


@pytest.mark.parametrize('style', ALL_STYLES)
def testClassAttributesWithSeparatedDocstrings(style: str) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/class_attributes/init_docstring.py',
        checkClassAttributes=True,
        allowInitDocstring=True,
        style=style,
    )
    expectedViolations = [
        'DOC601: Class `MyClass1`: Class docstring contains fewer class attributes '
        'than actual class attributes.  (Please read '
        'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
        'correctly document class attributes.)',
        'DOC603: Class `MyClass1`: Class docstring attributes are different from '
        'actual class attributes. (Or could be other formatting issues: '
        'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
        'Attributes in the class definition but not in the docstring: [hello: int, '
        'index: int, world: dict]. Arguments in the docstring but not in the actual '
        'class attributes: [indices: int]. (Please read '
        'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
        'correctly document class attributes.)',
        'DOC105: Method `MyClass1.__init__`: Argument names match, but type hints in '
        'these args do not match: arg1',
    ]
    assert list(map(str, violations)) == expectedViolations


@pytest.mark.parametrize(
    'filename',
    ['function.py', 'classmethod.py', 'method.py', 'staticmethod.py'],
)
@pytest.mark.parametrize('style', ALL_STYLES)
def testReturns(style: str, filename: str) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/returns/{filename}',
        skipCheckingShortDocstrings=True,
        requireReturnSectionWhenReturningNothing=True,
        style=style,
    )

    expectedViolations: list[str] = [
        'DOC201: Method `MyClass.func1_6` does not have a return section in '
        'docstring',
        'DOC203: Method `MyClass.func1_6` return type(s) in docstring not consistent with '
        'the return annotation. Return annotation has 1 type(s); docstring '
        'return section has 0 type(s).',
        'DOC101: Method `MyClass.func2`: Docstring contains fewer arguments than in '
        'function signature.',
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
        'are no return statements or annotations',
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
        'there are no return statements or annotations',
        'DOC203: Method `MyClass.func101` return type(s) in docstring not consistent '
        'with the return annotation. Return annotation has 0 type(s); docstring '
        'return section has 1 type(s).',
        'DOC201: Function `inner101` does not have a return section in docstring',
        'DOC203: Function `inner101` return type(s) in docstring not consistent with '
        'the return annotation. Return annotation has 1 type(s); docstring return '
        'section has 0 type(s).',
        'DOC203: Method `MyClass.zipLists1` return type(s) in docstring not consistent with '
        "the return annotation. Return annotation types: ['Iterator[Tuple[Any, "
        "Any]]']; docstring return section types: ['Iterator[Tuple[Any, int]]']",
    ])

    expectedViolationsCopy = copy.deepcopy(expectedViolations)
    if filename == 'function.py':
        _tweakViolationMsgForFunctions(expectedViolationsCopy)

    assert list(map(str, violations)) == expectedViolationsCopy


@pytest.mark.parametrize(
    'filename',
    ['function.py', 'classmethod.py', 'method.py', 'staticmethod.py'],
)
@pytest.mark.parametrize('style', ALL_STYLES)
@pytest.mark.skipif(
    pythonVersionBelow310(),
    reason='Python 3.9 does not support match-case syntax',
)
def testReturnsPy310plus(style: str, filename: str) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/returns/py310+/{filename}',
        skipCheckingShortDocstrings=True,
        requireReturnSectionWhenReturningNothing=True,
        style=style,
    )

    expectedViolations: list[str] = [
        'DOC201: Method `MyClass.func11` does not have a return section in docstring',
        'DOC203: Method `MyClass.func11` return type(s) in docstring not consistent '
        'with the return annotation. Return annotation has 1 type(s); docstring '
        'return section has 0 type(s).',
    ]

    expectedViolationsCopy = copy.deepcopy(expectedViolations)
    if filename == 'function.py':
        _tweakViolationMsgForFunctions(expectedViolationsCopy)

    assert list(map(str, violations)) == expectedViolationsCopy


@pytest.mark.parametrize('require', [False, True])
@pytest.mark.parametrize('style', ALL_STYLES)
def testReturns_returningNone(style: str, require: bool) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/returning_none/cases.py',
        skipCheckingShortDocstrings=True,
        requireReturnSectionWhenReturningNothing=require,
        style=style,
    )
    expectedViolationsCopy = (
        [
            'DOC201: Function `func` does not have a return section in docstring',
            'DOC203: Function `func` return type(s) in docstring not consistent with the '
            'return annotation. Return annotation has 1 type(s); docstring return section '
            'has 0 type(s).',
        ]
        if require
        else []
    )
    assert list(map(str, violations)) == expectedViolationsCopy


@pytest.mark.parametrize('require', [False, True])
@pytest.mark.parametrize('style', ALL_STYLES)
def testReturns_returningNoReturn(style: str, require: bool) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/returning_noreturn/cases.py',
        skipCheckingShortDocstrings=True,
        requireReturnSectionWhenReturningNothing=require,
        style=style,
    )
    expectedViolationsCopy = (
        [
            'DOC201: Function `func` does not have a return section in docstring',
            'DOC203: Function `func` return type(s) in docstring not consistent with the '
            'return annotation. Return annotation has 1 type(s); docstring return section '
            'has 0 type(s).',
        ]
        if require
        else []
    )
    assert list(map(str, violations)) == expectedViolationsCopy


def _tweakViolationMsgForFunctions(expectedViolationsCopy: list[str]) -> None:
    for i in range(len(expectedViolationsCopy)):
        expectedViolationsCopy[i] = expectedViolationsCopy[i].replace(
            'Method `MyClass.', 'Function `'
        )


expected_skipCheckingShortDocstrings_True = [
    'DOC101: Function `func3`: Docstring contains fewer arguments than in '
    'function signature.',
    'DOC106: Function `func3`: The option `--arg-type-hints-in-signature` is `True` '
    'but there are no argument type hints in the signature',
    'DOC107: Function `func3`: The option `--arg-type-hints-in-signature` is `True` '
    'but not all args in the signature have type hints',
    'DOC103: Function `func3`: Docstring arguments are different from function '
    'arguments. (Or could be other formatting issues: '
    'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the function signature but not in the '
    'docstring: [arg1: , arg2: , arg3: ]. Arguments in the docstring but not in '
    'the function signature: [var1: int, var2: str].',
]

expected_skipCheckingShortDocstrings_False = [
    'DOC101: Function `func1`: Docstring contains fewer arguments than in '
    'function signature.',
    'DOC106: Function `func1`: The option `--arg-type-hints-in-signature` is `True` '
    'but there are no argument type hints in the signature',
    'DOC107: Function `func1`: The option `--arg-type-hints-in-signature` is `True` '
    'but not all args in the signature have type hints',
    'DOC103: Function `func1`: Docstring arguments are different from function '
    'arguments. (Or could be other formatting issues: '
    'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the '
    'function signature but not in the docstring: [arg1: , arg2: , arg3: ].',
    'DOC201: Function `func1` does not have a return section in docstring',
    'DOC203: Function `func1` return type(s) in docstring not consistent with the '
    'return annotation. Return annotation has 1 type(s); docstring return section '
    'has 0 type(s).',
    'DOC101: Function `func2`: Docstring contains fewer arguments than in '
    'function signature.',
    'DOC106: Function `func2`: The option `--arg-type-hints-in-signature` is `True` '
    'but there are no argument type hints in the signature',
    'DOC107: Function `func2`: The option `--arg-type-hints-in-signature` is `True` '
    'but not all args in the signature have type hints',
    'DOC103: Function `func2`: Docstring arguments are different from function '
    'arguments. (Or could be other formatting issues: '
    'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the '
    'function signature but not in the docstring: [arg1: , arg2: , arg3: ].',
    'DOC201: Function `func2` does not have a return section in docstring',
    'DOC203: Function `func2` return type(s) in docstring not consistent with the '
    'return annotation. Return annotation has 1 type(s); docstring return section '
    'has 0 type(s).',
    'DOC101: Function `func3`: Docstring contains fewer arguments than in '
    'function signature.',
    'DOC106: Function `func3`: The option `--arg-type-hints-in-signature` is `True` '
    'but there are no argument type hints in the signature',
    'DOC107: Function `func3`: The option `--arg-type-hints-in-signature` is `True` '
    'but not all args in the signature have type hints',
    'DOC103: Function `func3`: Docstring arguments are different from function '
    'arguments. (Or could be other formatting issues: '
    'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the '
    'function signature but not in the docstring: [arg1: , arg2: , arg3: ]. '
    'Arguments in the docstring but not in the function signature: [var1: int, '
    'var2: str].',
]


@pytest.mark.parametrize(
    ('style', 'skipCheckingShortDocstrings', 'expected'),
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
        expected: list[str],
) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/short_docstrings/cases.py',
        skipCheckingShortDocstrings=skipCheckingShortDocstrings,
        checkReturnTypes=True,
        style=style,
    )
    assert list(map(str, violations)) == expected


@pytest.mark.parametrize('style', ALL_STYLES)
def testInit(style: str) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/init/init.py',
        style=style,
    )
    expected = [
        'DOC301: Class `A`: __init__() should not have a docstring; please combine it '
        'with the docstring of the class',
        'DOC302: Class `B`: The class docstring does not need a "Returns" section, '
        'because __init__() cannot return anything',
        'DOC105: Method `C.__init__`: Argument names match, but type hints in these '
        'args do not match: arg2',
        'DOC302: Class `C`: The class docstring does not need a "Returns" section, '
        'because __init__() cannot return anything',
        'DOC103: Method `D.__init__`: Docstring arguments are different from function '
        'arguments. (Or could be other formatting issues: '
        'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the function signature but not in the '
        'docstring: [arg1: int, arg2: float]. Arguments in the docstring but not in '
        'the function signature: [var1: list, var2: dict].',
        'DOC302: Class `D`: The class docstring does not need a "Returns" section, '
        'because __init__() cannot return anything',
    ]
    assert list(map(str, violations)) == expected


@pytest.mark.parametrize('style', ALL_STYLES)
def testAllowInitDocstring(style: str) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/allow_init_docstring/cases.py',
        style=style,
        allowInitDocstring=True,
    )
    expected = [
        'DOC304: Class `A`: Class docstring has an argument/parameter section; please '
        'put it in the __init__() docstring',
        'DOC302: Class `B`: The class docstring does not need a "Returns" section, '
        'because __init__() cannot return anything',
        'DOC303: Class `B`: The __init__() docstring does not need a "Returns" '
        'section, because it cannot return anything',
        'DOC304: Class `B`: Class docstring has an argument/parameter section; please '
        'put it in the __init__() docstring',
        'DOC302: Class `B`: The class docstring does not need a "Returns" section, '
        'because __init__() cannot return anything',
        'DOC305: Class `C`: Class docstring has a "Raises" section; please put it in '
        'the __init__() docstring',
        'DOC503: Method `C.__init__` exceptions in the "Raises" section in the '
        'docstring do not match those in the function body. Raised exceptions in the '
        "docstring: ['TypeError']. Raised exceptions in the body: ['ValueError'].",
        'DOC306: Class `D`: The class docstring does not need a "Yields" section, '
        'because __init__() cannot yield anything',
        'DOC307: Class `D`: The __init__() docstring does not need a "Yields" '
        'section, because __init__() cannot yield anything',
        'DOC306: Class `D`: The class docstring does not need a "Yields" section, '
        'because __init__() cannot yield anything',
        'DOC403: Method `D.__init__` has a "Yields" section in the docstring, but '
        'there are no "yield" statements, or the return annotation is not a '
        'Generator/Iterator/Iterable. (Or it could be because the function lacks a '
        'return annotation.)',
        'DOC602: Class `E`: Class docstring contains more class attributes than in '
        'actual class attributes.  (Please read '
        'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
        'correctly document class attributes.)',
        'DOC603: Class `E`: Class docstring attributes are different from actual '
        'class attributes. (Or could be other formatting issues: '
        'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
        'Arguments in the docstring but not in the actual class attributes: [attr1: , '
        'attr2: ]. (Please read '
        'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
        'correctly document class attributes.)',
    ]
    assert list(map(str, violations)) == expected


@pytest.mark.parametrize('style', ALL_STYLES)
def testYields(style: str) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/yields/cases.py',
        checkReturnTypes=False,
        style=style,
    )
    expected = [
        'DOC402: Method `A.method1` has "yield" statements, but the docstring does '
        'not have a "Yields" section',
        'DOC404: Method `A.method1` yield type(s) in docstring not consistent with '
        'the return annotation. Return annotation exists, but docstring "yields" '
        'section does not exist or has 0 type(s).',
        'DOC402: Method `A.method2` has "yield" statements, but the docstring does '
        'not have a "Yields" section',
        'DOC404: Method `A.method2` yield type(s) in docstring not consistent with '
        'the return annotation. Return annotation exists, but docstring "yields" '
        'section does not exist or has 0 type(s).',
        'DOC403: Method `A.method3` has a "Yields" section in the docstring, but '
        'there are no "yield" statements, or the return annotation is not a '
        'Generator/Iterator/Iterable. (Or it could be because the function lacks a '
        'return annotation.)',
        'DOC402: Method `A.method6` has "yield" statements, but the docstring does '
        'not have a "Yields" section',
        'DOC404: Method `A.method6` yield type(s) in docstring not consistent with '
        'the return annotation. Return annotation exists, but docstring "yields" '
        'section does not exist or has 0 type(s).',
        'DOC402: Method `A.method8a` has "yield" statements, but the docstring does '
        'not have a "Yields" section',
        'DOC404: Method `A.method8a` yield type(s) in docstring not consistent with '
        'the return annotation. Return annotation exists, but docstring "yields" '
        'section does not exist or has 0 type(s).',
        'DOC402: Method `A.method8b` has "yield" statements, but the docstring does '
        'not have a "Yields" section',
        'DOC404: Method `A.method8b` yield type(s) in docstring not consistent with '
        'the return annotation. Return annotation exists, but docstring "yields" '
        'section does not exist or has 0 type(s).',
        'DOC402: Method `A.method8c` has "yield" statements, but the docstring does '
        'not have a "Yields" section',
        'DOC404: Method `A.method8c` yield type(s) in docstring not consistent with '
        'the return annotation. Return annotation exists, but docstring "yields" '
        'section does not exist or has 0 type(s).',
        'DOC402: Method `A.method8d` has "yield" statements, but the docstring does '
        'not have a "Yields" section',
        'DOC404: Method `A.method8d` yield type(s) in docstring not consistent with '
        'the return annotation. Return annotation exists, but docstring "yields" '
        'section does not exist or has 0 type(s).',
        'DOC201: Method `A.zipLists2` does not have a return section in docstring',
        'DOC403: Method `A.zipLists2` has a "Yields" section in the docstring, but '
        'there are no "yield" statements, or the return annotation is not a '
        'Generator/Iterator/Iterable. (Or it could be because the function lacks a '
        'return annotation.)',
        'DOC404: Function `inner9a` yield type(s) in docstring not consistent with '
        'the return annotation. The yield type (the 0th arg in '
        'Generator[...]/Iterator[...]): str; docstring "yields" section types: '
        'Iterable[str]',
        'DOC402: Function `inner9b` has "yield" statements, but the docstring does '
        'not have a "Yields" section',
        'DOC404: Function `inner9b` yield type(s) in docstring not consistent with '
        'the return annotation. Return annotation exists, but docstring "yields" '
        'section does not exist or has 0 type(s).',
        'DOC201: Method `A.method9c` does not have a return section in docstring',
        'DOC403: Method `A.method9c` has a "Yields" section in the docstring, but '
        'there are no "yield" statements, or the return annotation is not a '
        'Generator/Iterator/Iterable. (Or it could be because the function lacks a '
        'return annotation.)',
        'DOC404: Function `inner9c` yield type(s) in docstring not consistent with '
        'the return annotation. The yield type (the 0th arg in '
        'Generator[...]/Iterator[...]): str; docstring "yields" section types: '
        'Iterable[str]',
        'DOC402: Method `A.method9d` has "yield" statements, but the docstring does '
        'not have a "Yields" section',
        'DOC404: Method `A.method9d` yield type(s) in docstring not consistent with '
        'the return annotation. Return annotation exists, but docstring "yields" '
        'section does not exist or has 0 type(s).',
        'DOC402: Function `inner9d` has "yield" statements, but the docstring does '
        'not have a "Yields" section',
        'DOC404: Function `inner9d` yield type(s) in docstring not consistent with '
        'the return annotation. Return annotation exists, but docstring "yields" '
        'section does not exist or has 0 type(s).',
        'DOC404: Method `A.method10a` yield type(s) in docstring not consistent with '
        'the return annotation. The yield type (the 0th arg in '
        'Generator[...]/Iterator[...]): str; docstring "yields" section types: int',
    ]
    assert list(map(str, violations)) == expected


@pytest.mark.parametrize('style', ALL_STYLES)
@pytest.mark.skipif(
    pythonVersionBelow310(),
    reason='Python 3.8 and 3.9 do not support match-case syntax',
)
def testYieldsPy310plus(style: str) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/yields/py310+/cases.py',
        checkReturnTypes=False,
        style=style,
    )
    expected = [
        'DOC402: Method `A.func10` has "yield" statements, but the docstring does not '
        'have a "Yields" section',
        'DOC404: Method `A.func10` yield type(s) in docstring not consistent with the '
        'return annotation. Return annotation exists, but docstring "yields" section '
        'does not exist or has 0 type(s).',
    ]
    assert list(map(str, violations)) == expected


@pytest.mark.parametrize('style', ALL_STYLES)
def testReturnAndYield(style: str) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/return_and_yield/cases.py',
        checkReturnTypes=True,
        checkYieldTypes=True,
        style=style,
    )
    expected = [
        'DOC405: Function `func2` has both "return" and "yield" statements. Please '
        'use Generator[YieldType, SendType, ReturnType] as the return type '
        'annotation, and put your yield type in YieldType and return type in '
        'ReturnType. More details in '
        'https://jsh9.github.io/pydoclint/notes_generator_vs_iterator.html',
        'DOC203: Function `func3` return type(s) in docstring not consistent with the '
        "return annotation. Return annotation types: ['float']; docstring return "
        "section types: ['str']",
        'DOC404: Function `func3` yield type(s) in docstring not consistent with the '
        'return annotation. The yield type (the 0th arg in '
        'Generator[...]/Iterator[...]): bool; docstring "yields" section types: int',
        'DOC203: Function `func4` return type(s) in docstring not consistent with the '
        "return annotation. Return annotation types: ['Generator']; docstring return "
        "section types: ['str']",
        'DOC404: Function `func4` yield type(s) in docstring not consistent with the '
        'return annotation. The yield type (the 0th arg in '
        'Generator[...]/Iterator[...]): Generator; docstring "yields" section types: '
        'int',
        'DOC405: Function `func5` has both "return" and "yield" statements. Please '
        'use Generator[YieldType, SendType, ReturnType] as the return type '
        'annotation, and put your yield type in YieldType and return type in '
        'ReturnType. More details in '
        'https://jsh9.github.io/pydoclint/notes_generator_vs_iterator.html',
        'DOC404: Function `func5` yield type(s) in docstring not consistent with the '
        'return annotation. The yield type (the 0th arg in '
        'Generator[...]/Iterator[...]): Iterator; docstring "yields" section types: '
        'int',
        # func9 documents the second Generator arg as a return type; PEP 696
        # makes that arg SendType, so DOC203 must still report a mismatch.
        'DOC203: Function `func9` return type(s) in docstring not consistent with the '
        "return annotation. Return annotation types: ['None']; docstring return "
        "section types: ['str']",
        'DOC201: Function `func10` does not have a return section in docstring',
        'DOC203: Function `func11` return type(s) in docstring not consistent with the '
        'return annotation. Return annotation types: '
        "['Generator[int, str, bool, bytes]']; docstring return section types: "
        "['bool']",
        'DOC404: Function `func11` yield type(s) in docstring not consistent with the '
        'return annotation. The yield type (the 0th arg in '
        'Generator[...]/Iterator[...]): Generator[int, str, bool, bytes]; '
        'docstring "yields" section types: int',
        'DOC203: Function `func12` return type(s) in docstring not consistent with the '
        "return annotation. Return annotation types: ['None']; docstring return "
        "section types: ['str']",
    ]
    assert list(map(str, violations)) == expected


@pytest.mark.parametrize('shouldDeclareAssertErr', [False, True])
@pytest.mark.parametrize('skipRaisesCheck', [False, True])
@pytest.mark.parametrize('style', ALL_STYLES)
def testRaises(
        style: str,
        skipRaisesCheck: bool,
        shouldDeclareAssertErr: bool,
) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/raises/cases.py',
        skipCheckingRaises=skipRaisesCheck,
        argTypeHintsInSignature=False,
        argTypeHintsInDocstring=False,
        checkReturnTypes=False,
        shouldDeclareAssertErrorIfAssertStatementExists=shouldDeclareAssertErr,
        style=style,
    )
    expected0 = [
        'DOC501: Method `B.func1` has raise statements, but the docstring does not '
        'have a "Raises" section',
        'DOC503: Method `B.func1` exceptions in the "Raises" section in the docstring '
        'do not match those in the function body. Raised exceptions in the docstring: []. '
        "Raised exceptions in the body: ['ValueError'].",
        'DOC503: Method `B.func4` exceptions in the "Raises" section in the docstring '
        'do not match those in the function body. Raised exceptions in the docstring: '
        "['CurtomError']. Raised exceptions in the body: ['CustomError'].",
        'DOC502: Method `B.func5` has a "Raises" section in the docstring, but there '
        'are not "raise" statements in the body',
        'DOC502: Method `B.func7` has a "Raises" section in the docstring, but there '
        'are not "raise" statements in the body',
        'DOC502: Method `B.func9a` has a "Raises" section in the docstring, but there '
        'are not "raise" statements in the body',
        'DOC501: Function `inner9a` has raise statements, but the docstring does '
        'not have a "Raises" section',
        'DOC503: Function `inner9a` exceptions in the "Raises" section in the '
        'docstring do not match those in the function body. Raised exceptions in the '
        "docstring: []. Raised exceptions in the body: ['FileNotFoundError'].",
        'DOC503: Method `B.func11` exceptions in the "Raises" section in the '
        'docstring do not match those in the function body. Raised exceptions in the '
        "docstring: ['TypeError']. Raised exceptions in the body: ['TypeError', "
        "'ValueError'].",
        'DOC503: Method `B.func13` exceptions in the "Raises" section in the '
        'docstring do not match those in the function body. Raised exceptions in the '
        "docstring: ['ValueError', 'ValueError']. Raised exceptions in the body: "
        "['ValueError'].",
        'DOC503: Method `B.func14` exceptions in the "Raises" section in the '
        'docstring do not match those in the function body. Raised exceptions in the '
        "docstring: ['CustomError']. Raised exceptions in the body: "
        "['exceptions.CustomError'].",
        'DOC503: Method `B.func15` exceptions in the "Raises" section in the '
        'docstring do not match those in the function body. Raised exceptions in the '
        "docstring: ['CustomError']. Raised exceptions in the body: "
        "['exceptions.m.CustomError'].",
    ]

    expectedTrue = [  # for if shouldDeclareAssertErr is True
        'DOC504: Method `B.func19` has assert statements, but the docstring does not '
        'have a "Raises" section. (Assert statements could raise "AssertError".)'
    ]

    expectedFalse = [  # for if shouldDeclareAssertErr is False
        'DOC502: Method `B.func17` has a "Raises" section in the docstring, but there '
        'are not "raise" statements in the body',
        'DOC502: Method `B.func18` has a "Raises" section in the docstring, but there '
        'are not "raise" statements in the body',
        'DOC502: Method `B.func20` has a "Raises" section in the docstring, but there '
        'are not "raise" statements in the body',
    ]

    expected1 = []
    expected = (
        expected1
        if skipRaisesCheck
        else (
            expected0
            + (expectedTrue if shouldDeclareAssertErr else expectedFalse)
        )
    )
    assert list(map(str, violations)) == expected


@pytest.mark.parametrize('skipRaisesCheck', [False, True])
@pytest.mark.parametrize('style', ALL_STYLES)
@pytest.mark.skipif(
    pythonVersionBelow310(),
    reason='Python 3.8 and 3.9 do not support match-case syntax',
)
def testRaisesPy310plus(style: str, skipRaisesCheck: bool) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/raises/py310+/cases.py',
        skipCheckingRaises=skipRaisesCheck,
        argTypeHintsInSignature=False,
        argTypeHintsInDocstring=False,
        checkReturnTypes=False,
        style=style,
    )
    expected0 = [
        'DOC501: Method `B.func10` has raise statements, but the docstring does not '
        'have a "Raises" section',
        'DOC503: Method `B.func10` exceptions in the "Raises" section in the '
        'docstring do not match those in the function body. Raised exceptions in the '
        "docstring: []. Raised exceptions in the body: ['ValueError'].",
    ]
    expected1 = []
    expected = expected1 if skipRaisesCheck else expected0
    assert list(map(str, violations)) == expected


@pytest.mark.parametrize('style', ALL_STYLES)
def testStarsInArgumentList(style: str) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/star_args/cases.py',
        style=style,
    )
    expected = [
        'DOC110: Function `func2`: The option `--arg-type-hints-in-docstring` is `True` '
        'but not all args in the docstring arg list have type hints',
        'DOC103: Function `func2`: Docstring arguments are different from function '
        'arguments. (Or could be other formatting issues: '
        'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the function signature but not in the '
        'docstring: [**kwargs: ]. Arguments in the docstring but not in the function '
        'signature: [kwargs: ].',
        'DOC110: Function `func4`: The option `--arg-type-hints-in-docstring` is `True` '
        'but not all args in the docstring arg list have type hints',
        'DOC103: Function `func4`: Docstring arguments are different from function '
        'arguments. (Or could be other formatting issues: '
        'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the function signature but not in the '
        'docstring: [*args: ]. Arguments in the docstring but not in the function '
        'signature: [args: ].',
        'DOC101: Function `func6`: Docstring contains fewer arguments than in '
        'function signature.',
        'DOC103: Function `func6`: Docstring arguments are different from function '
        'arguments. (Or could be other formatting issues: '
        'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). Arguments in the function signature but not in the '
        'docstring: [**kwargs: , *args: ].',
        'DOC101: Function `func7`: Docstring contains fewer arguments than in '
        'function signature.',
        'DOC103: Function `func7`: Docstring arguments are different from function '
        'arguments. (Or could be other formatting issues: '
        'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
        'Arguments in the function signature but not in the docstring: [**kwargs: , '
        '*args: ].',
    ]
    assert list(map(str, violations)) == expected


@pytest.mark.parametrize('style', ALL_STYLES)
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


@pytest.mark.parametrize('style', ALL_STYLES)
def testStarsInArgumentList3(style: str) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/star_args/cases3.py',
        style=style,
        omitStarsWhenDocumentingVarargs=True,
    )
    expected = [
        'DOC103: Function `func9`: Docstring arguments are different from function'
        ' arguments. (Or could be other formatting issues:'
        ' https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ).'
        ' Arguments in the function signature but not in the'
        ' docstring: [*args: int]. Arguments in the docstring but not in the function'
        ' signature: [**args: int].',
    ]
    assert list(map(str, violations)) == expected


def testParsingErrors_google() -> None:
    violations = _checkFile(
        filename=DATA_DIR / 'google/parsing_errors/cases.py',
        style='google',
        checkStyleMismatch=True,
        allowInitDocstring=True,
        checkClassAttributes=False,
    )
    # When there are parsing errors, only DOC001 is reported for the
    # malformed docstring; downstream checks are skipped.
    expected = [
        'DOC001: Function/method `__init__`: Potential formatting errors in '
        "docstring. Error message: Expected a colon in 'arg1'. (Note: DOC001 could "
        'trigger other unrelated violations under this function/method too. Please '
        'fix the docstring formatting first.)',
        'DOC001: Function/method `test`: Potential formatting errors in docstring. '
        'Error message: Parsed docstring parameter has an empty name (Note: DOC001 '
        'could trigger other unrelated violations under this function/method too. '
        'Please fix the docstring formatting first.)',
        'DOC001: Function/method `sphinx_type_directive`: Potential formatting '
        'errors in docstring. Error message: Parsed docstring parameter has an '
        'empty name (Note: DOC001 could trigger other unrelated violations under '
        'this function/method too. Please fix the docstring formatting first.)',
        'DOC001: Function/method `sphinx_param_with_type`: Potential formatting '
        'errors in docstring. Error message: Parsed docstring parameter has an '
        'empty name (Note: DOC001 could trigger other unrelated violations under '
        'this function/method too. Please fix the docstring formatting first.)',
        'DOC001: Function/method `empty_google_arg_name`: Potential formatting '
        'errors in docstring. Error message: Parsed docstring parameter has an '
        'empty name (Note: DOC001 could trigger other unrelated violations under '
        'this function/method too. Please fix the docstring formatting first.)',
        'DOC001: Class `BadClassDoc`: Potential formatting errors in docstring. '
        'Error message: Parsed docstring parameter has an empty name',
        'DOC001: Function/method `__init__`: Potential formatting errors in '
        'docstring. Error message: Parsed docstring parameter has an empty name '
        '(Note: DOC001 could trigger other unrelated violations under this '
        'function/method too. Please fix the docstring formatting first.)',
    ]
    assert list(map(str, violations)) == expected


def testParsingErrors_sphinx() -> None:
    violations = _checkFile(
        filename=DATA_DIR / 'sphinx/parsing_errors/cases.py',
        style='sphinx',
        checkStyleMismatch=True,
        allowInitDocstring=True,
        checkClassAttributes=False,
    )
    # When there are parsing errors, only DOC001 is reported for the
    # malformed docstring; downstream checks are skipped.
    expected = [
        'DOC001: Function/method `__init__`: Potential formatting errors in '
        'docstring. Error message: Expected one or two arguments for a param '
        'keyword. (Note: DOC001 could trigger other unrelated violations under this '
        'function/method too. Please fix the docstring formatting first.)',
        'DOC001: Function/method `emptyParamName`: Potential formatting errors in '
        'docstring. Error message: Expected one or two arguments for a param '
        'keyword. (Note: DOC001 could trigger other unrelated violations under '
        'this function/method too. Please fix the docstring formatting first.)',
        'DOC001: Function/method `missingParamDirectiveArgument`: Potential '
        'formatting errors in docstring. Error message: Expected one or two '
        'arguments for a param keyword. (Note: DOC001 could trigger other '
        'unrelated violations under this function/method too. Please fix the '
        'docstring formatting first.)',
        'DOC001: Class `BadClassDoc`: Potential formatting errors in docstring. '
        'Error message: Expected one or two arguments for a param keyword.',
        'DOC001: Function/method `__init__`: Potential formatting errors in '
        'docstring. Error message: Expected one or two arguments for a param '
        'keyword. (Note: DOC001 could trigger other unrelated violations under '
        'this function/method too. Please fix the docstring formatting first.)',
    ]
    assert list(map(str, violations)) == expected


def testParsingErrors_numpy() -> None:
    violations = _checkFile(
        filename=DATA_DIR / 'numpy/parsing_errors/cases.py',
        argTypeHintsInDocstring=False,
        argTypeHintsInSignature=False,
        style='numpy',
        checkStyleMismatch=True,
        allowInitDocstring=True,
        checkClassAttributes=False,
    )
    # When there are parsing errors, only DOC001 is reported for the
    # malformed docstring; downstream checks are skipped.
    expected = [
        'DOC001: Function/method `__init__`: Potential formatting errors in '
        "docstring. Error message: Section 'Parameters' is not empty but nothing was "
        'parsed. (Note: DOC001 could trigger other unrelated violations under this '
        'function/method too. Please fix the docstring formatting first.)',
        'DOC001: Function/method `method2`: Potential formatting errors in docstring. '
        "Error message: Section 'Yields' is not empty but nothing was parsed. (Note: "
        'DOC001 could trigger other unrelated violations under this function/method '
        'too. Please fix the docstring formatting first.)',
        'DOC003: Function/method `funcWithGoogleStyle`: Docstring style mismatch. '
        '(Please read more at https://jsh9.github.io/pydoclint/style_mismatch.html '
        '). You specified "numpy" style, but the docstring is likely not written '
        'in this style.',
        'DOC001: Function/method `missingParamName`: Potential formatting errors '
        "in docstring. Error message: Section 'Parameters' is not empty but "
        'nothing was parsed. (Note: DOC001 could trigger other unrelated '
        'violations under this function/method too. Please fix the docstring '
        'formatting first.)',
        'DOC001: Function/method `malformedRaisesSection`: Potential formatting '
        "errors in docstring. Error message: Section 'Raises' is not empty but "
        'nothing was parsed. (Note: DOC001 could trigger other unrelated '
        'violations under this function/method too. Please fix the docstring '
        'formatting first.)',
        'DOC001: Function/method `malformedYieldsSection`: Potential formatting '
        "errors in docstring. Error message: Section 'Yields' is not empty but "
        'nothing was parsed. (Note: DOC001 could trigger other unrelated '
        'violations under this function/method too. Please fix the docstring '
        'formatting first.)',
        'DOC001: Class `BadClassDoc`: Potential formatting errors in docstring. '
        "Error message: Section 'Parameters' is not empty but nothing was parsed.",
        'DOC001: Function/method `__init__`: Potential formatting errors in '
        "docstring. Error message: Section 'Parameters' is not empty but nothing "
        'was parsed. (Note: DOC001 could trigger other unrelated violations under '
        'this function/method too. Please fix the docstring formatting first.)',
        'DOC001: Function/method `__init__`: Potential formatting errors in '
        'docstring. Error message: Unsupported numpy docstring sections: '
        '"Inputs", "Outputs", "Properties", "🍔🥟🍕🌮🥦🍎🍊🌽🥭", "Side Effects" '
        '(Note: DOC001 could trigger other unrelated violations under this '
        'function/method too. Please fix the docstring formatting first.)',
    ]
    assert list(map(str, violations)) == expected


@pytest.mark.parametrize(
    ('expectedStyle', 'expectedViolations'),
    [
        (
            'google',
            [
                'DOC003: Function/method `func2a`: Docstring style mismatch. (Please read '
                'more at https://jsh9.github.io/pydoclint/style_mismatch.html ). You '
                'specified "google" style, but the docstring is likely not written in this '
                'style.',
                'DOC003: Function/method `func2b`: Docstring style mismatch. (Please read '
                'more at https://jsh9.github.io/pydoclint/style_mismatch.html ). You '
                'specified "google" style, but the docstring is likely not written in this '
                'style.',
                'DOC003: Function/method `func3a`: Docstring style mismatch. (Please read '
                'more at https://jsh9.github.io/pydoclint/style_mismatch.html ). You '
                'specified "google" style, but the docstring is likely not written in this '
                'style.',
                'DOC003: Function/method `func3b`: Docstring style mismatch. (Please read '
                'more at https://jsh9.github.io/pydoclint/style_mismatch.html ). You '
                'specified "google" style, but the docstring is likely not written in this '
                'style.',
            ],
        ),
        (
            'numpy',
            [
                'DOC003: Function/method `func1a`: Docstring style mismatch. (Please read '
                'more at https://jsh9.github.io/pydoclint/style_mismatch.html ). You '
                'specified "numpy" style, but the docstring is likely not written in this '
                'style.',
                'DOC003: Function/method `func1b`: Docstring style mismatch. (Please read '
                'more at https://jsh9.github.io/pydoclint/style_mismatch.html ). You '
                'specified "numpy" style, but the docstring is likely not written in this '
                'style.',
                'DOC003: Function/method `func3a`: Docstring style mismatch. (Please read '
                'more at https://jsh9.github.io/pydoclint/style_mismatch.html ). You '
                'specified "numpy" style, but the docstring is likely not written in this '
                'style.',
                'DOC003: Function/method `func3b`: Docstring style mismatch. (Please read '
                'more at https://jsh9.github.io/pydoclint/style_mismatch.html ). You '
                'specified "numpy" style, but the docstring is likely not written in this '
                'style.',
            ],
        ),
        (
            'sphinx',
            [
                'DOC003: Function/method `func1a`: Docstring style mismatch. (Please read '
                'more at https://jsh9.github.io/pydoclint/style_mismatch.html ). You '
                'specified "sphinx" style, but the docstring is likely not written in this '
                'style.',
                'DOC003: Function/method `func1b`: Docstring style mismatch. (Please read '
                'more at https://jsh9.github.io/pydoclint/style_mismatch.html ). You '
                'specified "sphinx" style, but the docstring is likely not written in this '
                'style.',
                'DOC003: Function/method `func2a`: Docstring style mismatch. (Please read '
                'more at https://jsh9.github.io/pydoclint/style_mismatch.html ). You '
                'specified "sphinx" style, but the docstring is likely not written in this '
                'style.',
                'DOC003: Function/method `func2b`: Docstring style mismatch. (Please read '
                'more at https://jsh9.github.io/pydoclint/style_mismatch.html ). You '
                'specified "sphinx" style, but the docstring is likely not written in this '
                'style.',
            ],
        ),
    ],
)
def testDocstringStyleMismatch(
        expectedStyle: str,
        expectedViolations: list[str],
) -> None:
    violations = _checkFile(
        filename=DATA_DIR / 'common/style_mismatch.py',
        style=expectedStyle,
        checkStyleMismatch=True,
    )
    assert list(map(str, violations)) == expectedViolations


@pytest.mark.parametrize('style', ALL_STYLES)
def testStyleMismatchIgnoresInlineSphinxKeywords(style: str) -> None:
    violations = _checkFile(
        filename=DATA_DIR / 'style_mismatch/this_can_be_any_style.py',
        style=style,
        checkStyleMismatch=True,
    )
    assert list(map(str, violations)) == []


@pytest.mark.parametrize(
    ('style', 'relative_path'),
    [
        ('numpy', 'numpy_pure.py'),
        ('google', 'google_pure.py'),
        ('sphinx', 'sphinx_pure.py'),
    ],
)
def testStyleMismatchAcceptsPureStyles(
        style: str,
        relative_path: str,
) -> None:
    violations = _checkFile(
        filename=DATA_DIR / 'style_mismatch' / relative_path,
        style=style,
        checkStyleMismatch=True,
    )
    assert not any('DOC003' in str(violation) for violation in violations)


@pytest.mark.parametrize('style', ALL_STYLES)
def testStyleMismatchFlagsMixedStyles(style: str) -> None:
    violations = _checkFile(
        filename=DATA_DIR / 'style_mismatch/mixed_styles.py',
        style=style,
        checkStyleMismatch=True,
    )
    assert any('DOC003' in str(violation) for violation in violations)


@pytest.mark.parametrize(
    'requireReturnSectionWhenReturningNothing', [False, True]
)
@pytest.mark.parametrize('style', ALL_STYLES)
def testNoReturnSection(
        style: str,
        requireReturnSectionWhenReturningNothing: bool,
) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/no_return_section/cases.py',
        style=style,
        checkReturnTypes=False,
        requireReturnSectionWhenReturningNothing=(
            requireReturnSectionWhenReturningNothing
        ),
    )
    expectedLookup = {
        True: [
            'DOC201: Function `func1` does not have a return section in docstring',
            'DOC201: Function `func2` does not have a return section in docstring',
            'DOC201: Function `func3` does not have a return section in docstring',
            'DOC201: Function `func4` does not have a return section in docstring',
            'DOC201: Function `func5` does not have a return section in docstring',
            'DOC201: Function `func7` does not have a return section in docstring',
            'DOC201: Function `func8` does not have a return section in docstring',
            'DOC201: Function `func9` does not have a return section in docstring',
            'DOC201: Function `func10` does not have a return section in docstring',
        ],
        False: [
            'DOC201: Function `func2` does not have a return section in docstring',
            'DOC201: Function `func3` does not have a return section in docstring',
            'DOC201: Function `func4` does not have a return section in docstring',
            'DOC201: Function `func5` does not have a return section in docstring',
            'DOC201: Function `func10` does not have a return section in docstring',
        ],
    }
    assert (
        list(map(str, violations))
        == expectedLookup[requireReturnSectionWhenReturningNothing]
    )


@pytest.mark.parametrize(
    'requireYieldSectionWhenYieldingNothing', [False, True]
)
@pytest.mark.parametrize('style', ALL_STYLES)
def testNoYieldSection(
        style: str,
        requireYieldSectionWhenYieldingNothing: bool,
) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/no_yield_section/cases.py',
        style=style,
        requireYieldSectionWhenYieldingNothing=(
            requireYieldSectionWhenYieldingNothing
        ),
    )
    expectedLookup = {
        True: [
            'DOC402: Function `func1` has "yield" statements, but the docstring does not '
            'have a "Yields" section',
            'DOC404: Function `func1` yield type(s) in docstring not consistent with the '
            'return annotation. Return annotation exists, but docstring "yields" section '
            'does not exist or has 0 type(s).',
            'DOC402: Function `func2` has "yield" statements, but the docstring does not '
            'have a "Yields" section',
            'DOC404: Function `func2` yield type(s) in docstring not consistent with the '
            'return annotation. Return annotation exists, but docstring "yields" section '
            'does not exist or has 0 type(s).',
            'DOC402: Function `func3` has "yield" statements, but the docstring does not '
            'have a "Yields" section',
            'DOC404: Function `func3` yield type(s) in docstring not consistent with the '
            'return annotation. Return annotation exists, but docstring "yields" section '
            'does not exist or has 0 type(s).',
        ],
        False: [
            'DOC402: Function `func3` has "yield" statements, but the docstring does not '
            'have a "Yields" section',
            'DOC404: Function `func3` yield type(s) in docstring not consistent with the '
            'return annotation. Return annotation exists, but docstring "yields" section '
            'does not exist or has 0 type(s).',
        ],
    }
    assert (
        list(map(str, violations))
        == expectedLookup[requireYieldSectionWhenYieldingNothing]
    )


@pytest.mark.parametrize('style', ALL_STYLES)
def testPropertyMethod(style: str) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/property_method/cases.py',
        style=style,
        skipCheckingShortDocstrings=True,
    )
    expected = []
    assert list(map(str, violations)) == expected


@pytest.mark.parametrize('checkReturnTypes', [False, True])
@pytest.mark.parametrize('style', ALL_STYLES)
def testAbstractMethod(style: str, checkReturnTypes: bool) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/abstract_method/cases.py',
        checkReturnTypes=checkReturnTypes,
        style=style,
    )
    if checkReturnTypes:
        expected = [
            'DOC201: Method `AbstractClass.another_abstract_method` does not have a '
            'return section in docstring',
            'DOC201: Method `AbstractClass.third_abstract_method` does not have a return '
            'section in docstring',
            'DOC203: Method `AbstractClass.third_abstract_method` return type(s) in '
            'docstring not consistent with the return annotation. Return annotation has 1 '
            'type(s); docstring return section has 0 type(s).',
        ]
    else:
        expected = [
            'DOC201: Method `AbstractClass.another_abstract_method` does not have a '
            'return section in docstring',
            'DOC201: Method `AbstractClass.third_abstract_method` does not have a return '
            'section in docstring',
        ]

    assert list(map(str, violations)) == expected


@pytest.mark.parametrize('style', ALL_STYLES)
def testNoReturnSectionInPropertyMethod(style: str) -> None:
    violations = _checkFile(
        filename=DATA_DIR / 'common/property_method.py',
        style=style,
        skipCheckingShortDocstrings=False,
        checkClassAttributes=False,
    )
    expected = [
        'DOC201: Method `MyOtherClass.method_2` does not have a return section in '
        'docstring',
        'DOC203: Method `MyOtherClass.method_2` return type(s) in docstring not '
        'consistent with the return annotation. Return annotation has 1 type(s); '
        'docstring return section has 0 type(s).',
        'DOC201: Method `MyOtherClass.method_3` does not have a return section in '
        'docstring',
        'DOC203: Method `MyOtherClass.method_3` return type(s) in docstring not '
        'consistent with the return annotation. Return annotation has 1 type(s); '
        'docstring return section has 0 type(s).',
    ]
    assert list(map(str, violations)) == expected


@pytest.mark.parametrize('argTypeHintsInSignature', [False, True])
@pytest.mark.parametrize('argTypeHintsInDocstring', [False, True])
@pytest.mark.parametrize('style', ALL_STYLES)
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

    expectedLookup = {
        (False, False): [
            'DOC108: Method `MyClass.func2`: The option `--arg-type-hints-in-signature` is '
            '`False` but there are argument type hints in the signature',
            'DOC111: Method `MyClass.func3`: The option `--arg-type-hints-in-docstring` is '
            '`False` but there are type hints in the docstring arg list',
            'DOC108: Method `MyClass.func4`: The option `--arg-type-hints-in-signature` is '
            '`False` but there are argument type hints in the signature',
            'DOC111: Method `MyClass.func4`: The option `--arg-type-hints-in-docstring` is '
            '`False` but there are type hints in the docstring arg list',
            'DOC108: Method `MyClass.func5`: The option `--arg-type-hints-in-signature` is '
            '`False` but there are argument type hints in the signature',
            'DOC111: Method `MyClass.func5`: The option `--arg-type-hints-in-docstring` is '
            '`False` but there are type hints in the docstring arg list',
            'DOC108: Method `MyClass.func6`: The option `--arg-type-hints-in-signature` is '
            '`False` but there are argument type hints in the signature',
            'DOC111: Method `MyClass.func6`: The option `--arg-type-hints-in-docstring` is '
            '`False` but there are type hints in the docstring arg list',
            'DOC108: Method `MyClass.func7`: The option `--arg-type-hints-in-signature` is '
            '`False` but there are argument type hints in the signature',
            'DOC111: Method `MyClass.func7`: The option `--arg-type-hints-in-docstring` is '
            '`False` but there are type hints in the docstring arg list',
        ],
        (False, True): [
            'DOC106: Method `MyClass.func1`: The option `--arg-type-hints-in-signature` is '
            '`True` but there are no argument type hints in the signature',
            'DOC107: Method `MyClass.func1`: The option `--arg-type-hints-in-signature` is '
            '`True` but not all args in the signature have type hints',
            'DOC106: Method `MyClass.func3`: The option `--arg-type-hints-in-signature` is '
            '`True` but there are no argument type hints in the signature',
            'DOC107: Method `MyClass.func3`: The option `--arg-type-hints-in-signature` is '
            '`True` but not all args in the signature have type hints',
            'DOC111: Method `MyClass.func3`: The option `--arg-type-hints-in-docstring` is '
            '`False` but there are type hints in the docstring arg list',
            'DOC111: Method `MyClass.func4`: The option `--arg-type-hints-in-docstring` is '
            '`False` but there are type hints in the docstring arg list',
            'DOC107: Method `MyClass.func5`: The option `--arg-type-hints-in-signature` is '
            '`True` but not all args in the signature have type hints',
            'DOC111: Method `MyClass.func5`: The option `--arg-type-hints-in-docstring` is '
            '`False` but there are type hints in the docstring arg list',
            'DOC111: Method `MyClass.func6`: The option `--arg-type-hints-in-docstring` is '
            '`False` but there are type hints in the docstring arg list',
            'DOC107: Method `MyClass.func7`: The option `--arg-type-hints-in-signature` is '
            '`True` but not all args in the signature have type hints',
            'DOC111: Method `MyClass.func7`: The option `--arg-type-hints-in-docstring` is '
            '`False` but there are type hints in the docstring arg list',
        ],
        (True, False): [
            'DOC109: Method `MyClass.func1`: The option `--arg-type-hints-in-docstring` is '
            '`True` but there are no type hints in the docstring arg list',
            'DOC110: Method `MyClass.func1`: The option `--arg-type-hints-in-docstring` is '
            '`True` but not all args in the docstring arg list have type hints',
            'DOC108: Method `MyClass.func2`: The option `--arg-type-hints-in-signature` is '
            '`False` but there are argument type hints in the signature',
            'DOC109: Method `MyClass.func2`: The option `--arg-type-hints-in-docstring` is '
            '`True` but there are no type hints in the docstring arg list',
            'DOC110: Method `MyClass.func2`: The option `--arg-type-hints-in-docstring` is '
            '`True` but not all args in the docstring arg list have type hints',
            'DOC108: Method `MyClass.func4`: The option `--arg-type-hints-in-signature` is '
            '`False` but there are argument type hints in the signature',
            'DOC108: Method `MyClass.func5`: The option `--arg-type-hints-in-signature` is '
            '`False` but there are argument type hints in the signature',
            'DOC110: Method `MyClass.func5`: The option `--arg-type-hints-in-docstring` is '
            '`True` but not all args in the docstring arg list have type hints',
            'DOC108: Method `MyClass.func6`: The option `--arg-type-hints-in-signature` is '
            '`False` but there are argument type hints in the signature',
            'DOC108: Method `MyClass.func7`: The option `--arg-type-hints-in-signature` is '
            '`False` but there are argument type hints in the signature',
            'DOC110: Method `MyClass.func7`: The option `--arg-type-hints-in-docstring` is '
            '`True` but not all args in the docstring arg list have type hints',
        ],
        (True, True): [
            'DOC106: Method `MyClass.func1`: The option `--arg-type-hints-in-signature` is '
            '`True` but there are no argument type hints in the signature',
            'DOC107: Method `MyClass.func1`: The option `--arg-type-hints-in-signature` is '
            '`True` but not all args in the signature have type hints',
            'DOC109: Method `MyClass.func1`: The option `--arg-type-hints-in-docstring` is '
            '`True` but there are no type hints in the docstring arg list',
            'DOC110: Method `MyClass.func1`: The option `--arg-type-hints-in-docstring` is '
            '`True` but not all args in the docstring arg list have type hints',
            'DOC109: Method `MyClass.func2`: The option `--arg-type-hints-in-docstring` is '
            '`True` but there are no type hints in the docstring arg list',
            'DOC110: Method `MyClass.func2`: The option `--arg-type-hints-in-docstring` is '
            '`True` but not all args in the docstring arg list have type hints',
            'DOC105: Method `MyClass.func2`: Argument names match, but type hints in '
            'these args do not match: arg1, arg2',
            'DOC106: Method `MyClass.func3`: The option `--arg-type-hints-in-signature` is '
            '`True` but there are no argument type hints in the signature',
            'DOC107: Method `MyClass.func3`: The option `--arg-type-hints-in-signature` is '
            '`True` but not all args in the signature have type hints',
            'DOC105: Method `MyClass.func3`: Argument names match, but type hints in '
            'these args do not match: arg1, arg2',
            'DOC107: Method `MyClass.func5`: The option `--arg-type-hints-in-signature` is '
            '`True` but not all args in the signature have type hints',
            'DOC110: Method `MyClass.func5`: The option `--arg-type-hints-in-docstring` is '
            '`True` but not all args in the docstring arg list have type hints',
            'DOC105: Method `MyClass.func5`: Argument names match, but type hints in '
            'these args do not match: arg1, arg2',
            'DOC105: Method `MyClass.func6`: Argument names match, but type hints in '
            'these args do not match: arg1',
            'DOC107: Method `MyClass.func7`: The option `--arg-type-hints-in-signature` is '
            '`True` but not all args in the signature have type hints',
            'DOC110: Method `MyClass.func7`: The option `--arg-type-hints-in-docstring` is '
            '`True` but not all args in the docstring arg list have type hints',
        ],
    }

    expected = expectedLookup[argTypeHintsInDocstring, argTypeHintsInSignature]
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


@pytest.mark.parametrize('checkArgDefaults', [False, True])
# no Sphinx style for now
@pytest.mark.parametrize('style', ['google', 'numpy'])
def testArgDefaults(
        style: str,
        checkArgDefaults: bool,
) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/arg_defaults/cases.py',
        style=style,
        argTypeHintsInDocstring=True,
        checkArgDefaults=checkArgDefaults,
    )

    expectedViolationsLookup = {
        True: [
            'DOC105: Function `func1`: Argument names match, but type hints in these args '
            'do not match: arg1, arg2 . (Note: docstring arg defaults should look like: '
            '`, default=XXX`)',
            'DOC105: Function `func4`: Argument names match, but type hints in these args '
            'do not match: arg1, arg2 . (Note: docstring arg defaults should look like: '
            '`, default=XXX`)',
            'DOC105: Function `func5`: Argument names match, but type hints in these args '
            'do not match: arg2, arg3 . (Note: docstring arg defaults should look like: '
            '`, default=XXX`)',
            'DOC105: Function `func7`: Argument names match, but type hints in these args '
            'do not match: arg2 . (Note: docstring arg defaults should look like: `, '
            'default=XXX`)',
            'DOC105: Method `MyClass.method1`: Argument names match, but type hints in '
            'these args do not match: arg1, arg2 . (Note: docstring arg defaults should '
            'look like: `, default=XXX`)',
            'DOC105: Method `MyClass.method3`: Argument names match, but type hints in '
            'these args do not match: arg1, arg2 . (Note: docstring arg defaults should '
            'look like: `, default=XXX`)',
            'DOC105: Function `wrong_default_style`: Argument names match, but type hints '
            'in these args do not match: arg2, arg3, arg4 . (Note: docstring arg defaults '
            'should look like: `, default=XXX`)',
            'DOC105: Function `default_string_double_quote`: Argument names match, but '
            'type hints in these args do not match: arg1 . (Note: docstring arg defaults '
            'should look like: `, default=XXX`)',
            'DOC105: Function `default_string_single_quote`: Argument names match, but '
            'type hints in these args do not match: arg1 . (Note: docstring arg defaults '
            'should look like: `, default=XXX`)',
        ],
        False: [
            'DOC105: Function `func2`: Argument names match, but type hints in these args '
            'do not match: arg1, arg2',
            'DOC105: Function `func3`: Argument names match, but type hints in these args '
            'do not match: arg1, arg2',
            'DOC105: Function `func4`: Argument names match, but type hints in these args '
            'do not match: arg1, arg2',
            'DOC105: Function `func5`: Argument names match, but type hints in these args '
            'do not match: arg1, arg2',
            'DOC105: Function `func6`: Argument names match, but type hints in these args '
            'do not match: arg2',
            'DOC105: Method `MyClass.method2`: Argument names match, but type hints in '
            'these args do not match: arg1, arg2',
            'DOC105: Method `MyClass.method3`: Argument names match, but type hints in '
            'these args do not match: arg1, arg2',
            'DOC105: Function `func_with_complex_defaults`: Argument names match, but '
            'type hints in these args do not match: arg2, arg3, arg4',
            'DOC105: Function `func_all_defaults`: Argument names match, but type hints '
            'in these args do not match: arg1, arg2, arg3',
            'DOC105: Function `func_single_quote_or_double_quote_dont_matter`: Argument '
            'names match, but type hints in these args do not match: arg1, arg2',
            'DOC105: Function `wrong_default_style`: Argument names match, but type hints '
            'in these args do not match: arg1, arg2, arg3, arg4',
            'DOC105: Function `space_does_not_matter`: Argument names match, but type '
            'hints in these args do not match: arg1',
            'DOC105: Function `default_string_double_quote`: Argument names match, but '
            'type hints in these args do not match: arg1, arg2, arg3',
            'DOC105: Function `default_string_single_quote`: Argument names match, but '
            'type hints in these args do not match: arg1, arg2, arg3',
        ],
    }

    assert (
        list(map(str, violations))
        == expectedViolationsLookup[checkArgDefaults]
    )


@pytest.mark.parametrize('argTypeHintsInDocstring', [False, True])
@pytest.mark.parametrize('requireInlineClassVarDocs', [False, True])
@pytest.mark.parametrize('style', ALL_STYLES)
def testInlineClassAttributeDocs(
        style: str,
        requireInlineClassVarDocs: bool,
        argTypeHintsInDocstring: bool,
) -> None:
    violations = _checkFile(
        filename=DATA_DIR / style / 'class_attributes/inline_docstring.py',
        style=style,
        requireInlineClassVarDocs=requireInlineClassVarDocs,
        argTypeHintsInDocstring=argTypeHintsInDocstring,
        skipCheckingShortDocstrings=False,
    )

    # (requireInlineClassVarDocs, argTypeHintsInDocstring) -> expected violations
    expectedViolationsLookup: dict[tuple[bool, bool], list[str]] = {
        (False, False): [
            'DOC606: Class `MyClass1`, Attribute `field1`: This attribute is documented '
            'inline, but it should be documented in the class docstring instead.',
            'DOC606: Class `MyClass1`, Attribute `field2`: This attribute is documented '
            'inline, but it should be documented in the class docstring instead.',
            'DOC606: Class `MyClass1`, Attribute `field3`: This attribute is documented '
            'inline, but it should be documented in the class docstring instead.',
            'DOC601: Class `MyClass1`: Class docstring contains fewer class attributes '
            'than actual class attributes.  (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
            'DOC603: Class `MyClass1`: Class docstring attributes are different from '
            'actual class attributes. (Or could be other formatting issues: '
            'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
            'Attributes in the class definition but not in the docstring: '
            '[field1: int, field2: str, field3: list[int]]. (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
            'DOC606: Class `MyClass2`, Attribute `documented_field`: This attribute is '
            'documented inline, but it should be documented in the class docstring '
            'instead.',
            'DOC601: Class `MyClass2`: Class docstring contains fewer class attributes '
            'than actual class attributes.  (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
            'DOC603: Class `MyClass2`: Class docstring attributes are different from '
            'actual class attributes. (Or could be other formatting issues: '
            'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
            'Attributes in the class definition but not in the docstring: '
            '[documented_field: float, undocumented_field: bool]. (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
            'DOC606: Class `MyClass3`, Attribute `field2`: This attribute is documented '
            'inline, but it should be documented in the class docstring instead.',
            'DOC606: Class `MyClass3`, Attribute `field3`: This attribute is documented '
            'inline, but it should be documented in the class docstring instead.',
            'DOC606: Class `MyClass3`, Attribute `field4`: This attribute is documented '
            'inline, but it should be documented in the class docstring instead.',
            'DOC606: Class `MyClass3`, Attribute `field5`: This attribute is documented '
            'inline, but it should be documented in the class docstring instead.',
            'DOC601: Class `MyClass3`: Class docstring contains fewer class attributes '
            'than actual class attributes.  (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
            'DOC603: Class `MyClass3`: Class docstring attributes are different from '
            'actual class attributes. (Or could be other formatting issues: '
            'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
            'Attributes in the class definition but not in the docstring: '
            '[field2: str, field3: int, field4: bool]. (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
            'DOC606: Class `MyClass4`, Attribute `field1`: This attribute is documented '
            'inline, but it should be documented in the class docstring instead.',
            'DOC601: Class `MyClass4`: Class docstring contains fewer class attributes '
            'than actual class attributes.  (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
            'DOC603: Class `MyClass4`: Class docstring attributes are different from '
            'actual class attributes. (Or could be other formatting issues: '
            'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
            'Attributes in the class definition but not in the docstring: '
            '[field1: str]. (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
        ],
        (False, True): [
            'DOC606: Class `MyClass1`, Attribute `field1`: This attribute is documented '
            'inline, but it should be documented in the class docstring instead.',
            'DOC606: Class `MyClass1`, Attribute `field2`: This attribute is documented '
            'inline, but it should be documented in the class docstring instead.',
            'DOC606: Class `MyClass1`, Attribute `field3`: This attribute is documented '
            'inline, but it should be documented in the class docstring instead.',
            'DOC601: Class `MyClass1`: Class docstring contains fewer class attributes '
            'than actual class attributes.  (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
            'DOC603: Class `MyClass1`: Class docstring attributes are different from '
            'actual class attributes. (Or could be other formatting issues: '
            'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
            'Attributes in the class definition but not in the docstring: '
            '[field1: int, field2: str, field3: list[int]]. (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
            'DOC606: Class `MyClass2`, Attribute `documented_field`: This attribute is '
            'documented inline, but it should be documented in the class docstring '
            'instead.',
            'DOC601: Class `MyClass2`: Class docstring contains fewer class attributes '
            'than actual class attributes.  (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
            'DOC603: Class `MyClass2`: Class docstring attributes are different from '
            'actual class attributes. (Or could be other formatting issues: '
            'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
            'Attributes in the class definition but not in the docstring: '
            '[documented_field: float, undocumented_field: bool]. (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
            'DOC606: Class `MyClass3`, Attribute `field2`: This attribute is documented '
            'inline, but it should be documented in the class docstring instead.',
            'DOC606: Class `MyClass3`, Attribute `field3`: This attribute is documented '
            'inline, but it should be documented in the class docstring instead.',
            'DOC606: Class `MyClass3`, Attribute `field4`: This attribute is documented '
            'inline, but it should be documented in the class docstring instead.',
            'DOC606: Class `MyClass3`, Attribute `field5`: This attribute is documented '
            'inline, but it should be documented in the class docstring instead.',
            'DOC601: Class `MyClass3`: Class docstring contains fewer class attributes '
            'than actual class attributes.  (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
            'DOC603: Class `MyClass3`: Class docstring attributes are different from '
            'actual class attributes. (Or could be other formatting issues: '
            'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
            'Attributes in the class definition but not in the docstring: '
            '[field2: str, field3: int, field4: bool]. (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
            'DOC606: Class `MyClass4`, Attribute `field1`: This attribute is documented '
            'inline, but it should be documented in the class docstring instead.',
            'DOC601: Class `MyClass4`: Class docstring contains fewer class attributes '
            'than actual class attributes.  (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
            'DOC603: Class `MyClass4`: Class docstring attributes are different from '
            'actual class attributes. (Or could be other formatting issues: '
            'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
            'Attributes in the class definition but not in the docstring: '
            '[field1: str]. (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
        ],
        (True, False): [
            'DOC601: Class `MyClass2`: Class docstring contains fewer class attributes '
            'than actual class attributes.  (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
            'DOC603: Class `MyClass2`: Class docstring attributes are different from '
            'actual class attributes. (Or could be other formatting issues: '
            'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
            'Attributes in the class definition but not documented inline: '
            '[undocumented_field: bool]. (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
            'DOC607: Class `MyClass3`: The class docstring does not need an "Attributes" '
            'section, because the class attributes are documented inline.',
            'DOC601: Class `MyClass3`: Class docstring contains fewer class attributes '
            'than actual class attributes.  (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
            'DOC603: Class `MyClass3`: Class docstring attributes are different from '
            'actual class attributes. (Or could be other formatting issues: '
            'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
            'Attributes in the class definition but not documented inline: '
            '[field1: int]. (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
        ],
        (True, True): [
            'DOC601: Class `MyClass2`: Class docstring contains fewer class attributes '
            'than actual class attributes.  (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
            'DOC603: Class `MyClass2`: Class docstring attributes are different from '
            'actual class attributes. (Or could be other formatting issues: '
            'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
            'Attributes in the class definition but not documented inline: '
            '[undocumented_field: bool]. (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
            'DOC607: Class `MyClass3`: The class docstring does not need an "Attributes" '
            'section, because the class attributes are documented inline.',
            'DOC601: Class `MyClass3`: Class docstring contains fewer class attributes '
            'than actual class attributes.  (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
            'DOC603: Class `MyClass3`: Class docstring attributes are different from '
            'actual class attributes. (Or could be other formatting issues: '
            'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
            'Attributes in the class definition but not documented inline: '
            '[field1: int]. (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
            'DOC605: Class `MyClass4`: Attribute names match, but type hints in these '
            'attributes do not match: field1  (Please read '
            'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
            'correctly document class attributes.)',
        ],
    }

    assert (
        list(map(str, violations))
        == expectedViolationsLookup[
            requireInlineClassVarDocs, argTypeHintsInDocstring
        ]
    )


@pytest.mark.parametrize(
    (
        'ignorePrivateClassAttributes',
        'ignoreUnderscoreOnlyClassAttributes',
        'ignoreSpecialDunderClassAttributes',
        'expectedViolationMessages',
    ),
    [
        (True, True, True, []),
        (
            True,
            True,
            False,
            [
                'DOC601: Class `Example`: Class docstring contains fewer class'
                ' attributes than actual class attributes.  (Please read'
                ' https://jsh9.github.io/pydoclint/checking_class_attributes.html'
                ' on how to correctly document class attributes.)',
                'DOC603: Class `Example`: Class docstring attributes are'
                ' different from actual class attributes. (Or could be other'
                ' formatting issues:'
                ' https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103'
                ' ). Attributes in the class definition but not in the'
                ' docstring: [__tablename__: str]. (Please read'
                ' https://jsh9.github.io/pydoclint/checking_class_attributes.html'
                ' on how to correctly document class attributes.)',
            ],
        ),
        (
            True,
            False,
            True,
            [
                'DOC601: Class `Example`: Class docstring contains fewer class'
                ' attributes than actual class attributes.  (Please read'
                ' https://jsh9.github.io/pydoclint/checking_class_attributes.html'
                ' on how to correctly document class attributes.)',
                'DOC603: Class `Example`: Class docstring attributes are'
                ' different from actual class attributes. (Or could be other'
                ' formatting issues:'
                ' https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103'
                ' ). Attributes in the class definition but not in the'
                ' docstring: [_: bool, __: float]. (Please read'
                ' https://jsh9.github.io/pydoclint/checking_class_attributes.html'
                ' on how to correctly document class attributes.)',
            ],
        ),
        (
            True,
            False,
            False,
            [
                'DOC601: Class `Example`: Class docstring contains fewer class'
                ' attributes than actual class attributes.  (Please read'
                ' https://jsh9.github.io/pydoclint/checking_class_attributes.html'
                ' on how to correctly document class attributes.)',
                'DOC603: Class `Example`: Class docstring attributes are'
                ' different from actual class attributes. (Or could be other'
                ' formatting issues:'
                ' https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103'
                ' ). Attributes in the class definition but not in the'
                ' docstring: [_: bool, __: float, __tablename__: str]. (Please'
                ' read'
                ' https://jsh9.github.io/pydoclint/checking_class_attributes.html'
                ' on how to correctly document class attributes.)',
            ],
        ),
        (
            False,
            True,
            True,
            [
                'DOC601: Class `Example`: Class docstring contains fewer class'
                ' attributes than actual class attributes.  (Please read'
                ' https://jsh9.github.io/pydoclint/checking_class_attributes.html'
                ' on how to correctly document class attributes.)',
                'DOC603: Class `Example`: Class docstring attributes are'
                ' different from actual class attributes. (Or could be other'
                ' formatting issues:'
                ' https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103'
                ' ). Attributes in the class definition but not in the'
                ' docstring: [_private: str]. (Please read'
                ' https://jsh9.github.io/pydoclint/checking_class_attributes.html'
                ' on how to correctly document class attributes.)',
            ],
        ),
        (
            False,
            True,
            False,
            [
                'DOC601: Class `Example`: Class docstring contains fewer class'
                ' attributes than actual class attributes.  (Please read'
                ' https://jsh9.github.io/pydoclint/checking_class_attributes.html'
                ' on how to correctly document class attributes.)',
                'DOC603: Class `Example`: Class docstring attributes are'
                ' different from actual class attributes. (Or could be other'
                ' formatting issues:'
                ' https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103'
                ' ). Attributes in the class definition but not in the'
                ' docstring: [__tablename__: str, _private: str]. (Please read'
                ' https://jsh9.github.io/pydoclint/checking_class_attributes.html'
                ' on how to correctly document class attributes.)',
            ],
        ),
        (
            False,
            False,
            True,
            [
                'DOC601: Class `Example`: Class docstring contains fewer class'
                ' attributes than actual class attributes.  (Please read'
                ' https://jsh9.github.io/pydoclint/checking_class_attributes.html'
                ' on how to correctly document class attributes.)',
                'DOC603: Class `Example`: Class docstring attributes are'
                ' different from actual class attributes. (Or could be other'
                ' formatting issues:'
                ' https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103'
                ' ). Attributes in the class definition but not in the'
                ' docstring: [_: bool, __: float, _private: str]. (Please read'
                ' https://jsh9.github.io/pydoclint/checking_class_attributes.html'
                ' on how to correctly document class attributes.)',
            ],
        ),
        (
            False,
            False,
            False,
            [
                'DOC601: Class `Example`: Class docstring contains fewer class'
                ' attributes than actual class attributes.  (Please read'
                ' https://jsh9.github.io/pydoclint/checking_class_attributes.html'
                ' on how to correctly document class attributes.)',
                'DOC603: Class `Example`: Class docstring attributes are'
                ' different from actual class attributes. (Or could be other'
                ' formatting issues:'
                ' https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103'
                ' ). Attributes in the class definition but not in the'
                ' docstring: [_: bool, __: float, __tablename__: str, _private:'
                ' str]. (Please read'
                ' https://jsh9.github.io/pydoclint/checking_class_attributes.html'
                ' on how to correctly document class attributes.)',
            ],
        ),
    ],
)
def testClassAttributeNameCategoryOptions(
        ignorePrivateClassAttributes: bool,
        ignoreUnderscoreOnlyClassAttributes: bool,
        ignoreSpecialDunderClassAttributes: bool,
        expectedViolationMessages: list[str],
) -> None:
    """Ensure the three class-attribute name options work together."""
    violations = _checkFile(
        filename=(DATA_DIR / 'name_category_options/class_attributes.py'),
        style='numpy',
        argTypeHintsInDocstring=False,
        ignorePrivateClassAttributes=ignorePrivateClassAttributes,
        ignoreUnderscoreOnlyClassAttributes=(
            ignoreUnderscoreOnlyClassAttributes
        ),
        ignoreSpecialDunderClassAttributes=ignoreSpecialDunderClassAttributes,
    )
    assert list(map(str, violations)) == expectedViolationMessages


@pytest.mark.parametrize(
    (
        'ignorePrivateArgs',
        'ignoreUnderscoreOnlyArgs',
        'ignoreSpecialDunderArgs',
        'expectedViolationMessages',
    ),
    [
        (True, True, True, []),
        (
            True,
            True,
            False,
            [
                'DOC101: Function `function_1`: Docstring contains fewer'
                ' arguments than in function signature.',
                'DOC103: Function `function_1`: Docstring arguments are'
                ' different from function arguments. (Or could be other'
                ' formatting issues:'
                ' https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103'
                ' ). Arguments in the function signature but not in the'
                ' docstring: [__special__: str].',
                'DOC101: Function `function_2`: Docstring contains fewer'
                ' arguments than in function signature.',
                'DOC103: Function `function_2`: Docstring arguments are'
                ' different from function arguments. (Or could be other'
                ' formatting issues:'
                ' https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103'
                ' ). Arguments in the function signature but not in the'
                ' docstring: [**__special__: str].',
            ],
        ),
        (
            True,
            False,
            True,
            [
                'DOC101: Function `function_1`: Docstring contains fewer'
                ' arguments than in function signature.',
                'DOC103: Function `function_1`: Docstring arguments are'
                ' different from function arguments. (Or could be other'
                ' formatting issues:'
                ' https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103'
                ' ). Arguments in the function signature but not in the'
                ' docstring: [_: float, __: bool].',
                'DOC101: Function `function_2`: Docstring contains fewer'
                ' arguments than in function signature.',
                'DOC103: Function `function_2`: Docstring arguments are'
                ' different from function arguments. (Or could be other'
                ' formatting issues:'
                ' https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103'
                ' ). Arguments in the function signature but not in the'
                ' docstring: [*_: int].',
                'DOC101: Function `function_3`: Docstring contains fewer'
                ' arguments than in function signature.',
                'DOC103: Function `function_3`: Docstring arguments are'
                ' different from function arguments. (Or could be other'
                ' formatting issues:'
                ' https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103'
                ' ). Arguments in the function signature but not in the'
                ' docstring: [**__: str].',
            ],
        ),
        (
            True,
            False,
            False,
            [
                'DOC101: Function `function_1`: Docstring contains fewer'
                ' arguments than in function signature.',
                'DOC103: Function `function_1`: Docstring arguments are'
                ' different from function arguments. (Or could be other'
                ' formatting issues:'
                ' https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103'
                ' ). Arguments in the function signature but not in the'
                ' docstring: [_: float, __: bool, __special__: str].',
                'DOC101: Function `function_2`: Docstring contains fewer'
                ' arguments than in function signature.',
                'DOC103: Function `function_2`: Docstring arguments are'
                ' different from function arguments. (Or could be other'
                ' formatting issues:'
                ' https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103'
                ' ). Arguments in the function signature but not in the'
                ' docstring: [**__special__: str, *_: int].',
                'DOC101: Function `function_3`: Docstring contains fewer'
                ' arguments than in function signature.',
                'DOC103: Function `function_3`: Docstring arguments are'
                ' different from function arguments. (Or could be other'
                ' formatting issues:'
                ' https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103'
                ' ). Arguments in the function signature but not in the'
                ' docstring: [**__: str].',
            ],
        ),
        (
            False,
            True,
            True,
            [
                'DOC101: Function `function_1`: Docstring contains fewer'
                ' arguments than in function signature.',
                'DOC103: Function `function_1`: Docstring arguments are'
                ' different from function arguments. (Or could be other'
                ' formatting issues:'
                ' https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103'
                ' ). Arguments in the function signature but not in the'
                ' docstring: [__d: list, _c: dict].',
                'DOC101: Function `function_3`: Docstring contains fewer'
                ' arguments than in function signature.',
                'DOC103: Function `function_3`: Docstring arguments are'
                ' different from function arguments. (Or could be other'
                ' formatting issues:'
                ' https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103'
                ' ). Arguments in the function signature but not in the'
                ' docstring: [*_private: int].',
            ],
        ),
        (
            False,
            True,
            False,
            [
                'DOC101: Function `function_1`: Docstring contains fewer'
                ' arguments than in function signature.',
                'DOC103: Function `function_1`: Docstring arguments are'
                ' different from function arguments. (Or could be other'
                ' formatting issues:'
                ' https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103'
                ' ). Arguments in the function signature but not in the'
                ' docstring: [__d: list, __special__: str, _c: dict].',
                'DOC101: Function `function_2`: Docstring contains fewer'
                ' arguments than in function signature.',
                'DOC103: Function `function_2`: Docstring arguments are'
                ' different from function arguments. (Or could be other'
                ' formatting issues:'
                ' https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103'
                ' ). Arguments in the function signature but not in the'
                ' docstring: [**__special__: str].',
                'DOC101: Function `function_3`: Docstring contains fewer'
                ' arguments than in function signature.',
                'DOC103: Function `function_3`: Docstring arguments are'
                ' different from function arguments. (Or could be other'
                ' formatting issues:'
                ' https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103'
                ' ). Arguments in the function signature but not in the'
                ' docstring: [*_private: int].',
            ],
        ),
        (
            False,
            False,
            True,
            [
                'DOC101: Function `function_1`: Docstring contains fewer'
                ' arguments than in function signature.',
                'DOC103: Function `function_1`: Docstring arguments are'
                ' different from function arguments. (Or could be other'
                ' formatting issues:'
                ' https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103'
                ' ). Arguments in the function signature but not in the'
                ' docstring: [_: float, __: bool, __d: list, _c: dict].',
                'DOC101: Function `function_2`: Docstring contains fewer'
                ' arguments than in function signature.',
                'DOC103: Function `function_2`: Docstring arguments are'
                ' different from function arguments. (Or could be other'
                ' formatting issues:'
                ' https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103'
                ' ). Arguments in the function signature but not in the'
                ' docstring: [*_: int].',
                'DOC101: Function `function_3`: Docstring contains fewer'
                ' arguments than in function signature.',
                'DOC103: Function `function_3`: Docstring arguments are'
                ' different from function arguments. (Or could be other'
                ' formatting issues:'
                ' https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103'
                ' ). Arguments in the function signature but not in the'
                ' docstring: [**__: str, *_private: int].',
            ],
        ),
        (
            False,
            False,
            False,
            [
                'DOC101: Function `function_1`: Docstring contains fewer'
                ' arguments than in function signature.',
                'DOC103: Function `function_1`: Docstring arguments are'
                ' different from function arguments. (Or could be other'
                ' formatting issues:'
                ' https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103'
                ' ). Arguments in the function signature but not in the'
                ' docstring: [_: float, __: bool, __d: list, __special__:'
                ' str, _c: dict].',
                'DOC101: Function `function_2`: Docstring contains fewer'
                ' arguments than in function signature.',
                'DOC103: Function `function_2`: Docstring arguments are'
                ' different from function arguments. (Or could be other'
                ' formatting issues:'
                ' https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103'
                ' ). Arguments in the function signature but not in the'
                ' docstring: [**__special__: str, *_: int].',
                'DOC101: Function `function_3`: Docstring contains fewer'
                ' arguments than in function signature.',
                'DOC103: Function `function_3`: Docstring arguments are'
                ' different from function arguments. (Or could be other'
                ' formatting issues:'
                ' https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103'
                ' ). Arguments in the function signature but not in the'
                ' docstring: [**__: str, *_private: int].',
            ],
        ),
    ],
)
def testFunctionArgumentNameCategoryOptions(
        ignorePrivateArgs: bool,
        ignoreUnderscoreOnlyArgs: bool,
        ignoreSpecialDunderArgs: bool,
        expectedViolationMessages: list[str],
) -> None:
    """Ensure the three argument name options work together."""
    violations = _checkFile(
        filename=(DATA_DIR / 'name_category_options/function_arguments.py'),
        style='google',
        argTypeHintsInDocstring=False,
        ignorePrivateArgs=ignorePrivateArgs,
        ignoreUnderscoreOnlyArgs=ignoreUnderscoreOnlyArgs,
        ignoreSpecialDunderArgs=ignoreSpecialDunderArgs,
    )
    assert list(map(str, violations)) == expectedViolationMessages


@pytest.mark.parametrize(
    (
        'ignorePrivateClassAttributes',
        'ignoreUnderscoreOnlyClassAttributes',
        'ignoreSpecialDunderClassAttributes',
        'expectedExtraNames',
    ),
    [
        (True, True, True, ['_private', '_', '__', '__tablename__']),
        (True, True, False, ['_private', '_', '__']),
        (True, False, True, ['_private', '__tablename__']),
        (True, False, False, ['_private']),
        (False, True, True, ['_', '__', '__tablename__']),
        (False, True, False, ['_', '__']),
        (False, False, True, ['__tablename__']),
        (False, False, False, []),
    ],
)
def testIgnoredClassAttributeNamesAreExactExtras(
        ignorePrivateClassAttributes: bool,
        ignoreUnderscoreOnlyClassAttributes: bool,
        ignoreSpecialDunderClassAttributes: bool,
        expectedExtraNames: list[str],
) -> None:
    """Ensure every ignored class attribute is reported as an extra."""
    violations = _checkFile(
        filename=(
            DATA_DIR
            / 'name_category_options'
            / 'documented_class_attributes.py'
        ),
        style='numpy',
        argTypeHintsInDocstring=False,
        ignorePrivateClassAttributes=ignorePrivateClassAttributes,
        ignoreUnderscoreOnlyClassAttributes=(
            ignoreUnderscoreOnlyClassAttributes
        ),
        ignoreSpecialDunderClassAttributes=ignoreSpecialDunderClassAttributes,
    )
    if not expectedExtraNames:
        assert violations == []
        return

    assert [violation.fullErrorCode for violation in violations] == [
        'DOC602',
        'DOC603',
    ]
    actualExtraArgs = (
        str(violations[1])
        .split(
            'Arguments in the docstring but not in the actual class attributes: [',
            maxsplit=1,
        )[1]
        .split('].', maxsplit=1)[0]
        .split(', ')
    )
    actualExtraNames = [
        arg.split(':', maxsplit=1)[0] for arg in actualExtraArgs
    ]
    assert sorted(actualExtraNames) == sorted(expectedExtraNames)

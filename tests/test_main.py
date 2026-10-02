import copy
import shutil
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

from pydoclint.main import _checkFile, _checkPaths
from pydoclint.main import main as cliMain

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
            'DOC201: Method `AbstractClass.third_abstract_method` does not have a return '
            'section in docstring',
            'DOC203: Method `AbstractClass.third_abstract_method` return type(s) in '
            'docstring not consistent with the return annotation. Return annotation has 1 '
            'type(s); docstring return section has 0 type(s).',
            'DOC201: Method `AbstractClass.abstractIteratorThatReturns` does not have'
            ' a return section in docstring',
            'DOC203: Method `AbstractClass.abstractMethodWithoutReturnAnnotation` return'
            ' type(s) in docstring not consistent with the return annotation. Return'
            ' annotation has 0 type(s); docstring return section has 1 type(s).',
        ]
    else:
        expected = [
            'DOC201: Method `AbstractClass.third_abstract_method` does not have a return '
            'section in docstring',
            'DOC201: Method `AbstractClass.abstractIteratorThatReturns` does not have'
            ' a return section in docstring',
        ]

    assert list(map(str, violations)) == expected


@pytest.mark.parametrize('suffix', ['.py', '.pyi'])
@pytest.mark.parametrize('style', ALL_STYLES)
def testStubFile(tmp_path: Path, style: str, suffix: str) -> None:
    """
    Test that functions in stub (.pyi) files are checked without relying on
    their placeholder bodies (``...``).

    The same fixture is checked twice: as a .py file and as a .pyi file. Only
    the file suffix differs, so comparing the two expected lists shows what
    changes for stubs. Violations that come only from the placeholder body
    (such as DOC502 for a "Raises" section without "raise" statements) are
    reported for .py but not for .pyi. Violations that don't depend on the body
    (such as DOC105 for a wrong argument type) are reported for both.
    """
    filename = tmp_path / f'cases{suffix}'
    shutil.copyfile(DATA_DIR / f'{style}/stub_file/cases.pyi', filename)
    violations = _checkFile(filename=filename, style=style)
    expectedLookup = {
        '.py': [
            'DOC502: Method `StubClass.documentsRaises` has a "Raises" section in the'
            ' docstring, but there are not "raise" statements in the body',
            'DOC403: Method `StubClass.documentsYields` has a "Yields" section in the'
            ' docstring, but there are no "yield" statements, or the return annotation is'
            ' not a Generator/Iterator/Iterable. (Or it could be because the function'
            ' lacks a return annotation.)',
            'DOC201: Method `StubClass.documentsYieldsWithIterator` does not have a'
            ' return section in docstring',
            'DOC403: Method `StubClass.documentsYieldsWithIterator` has a "Yields"'
            ' section in the docstring, but there are no "yield" statements, or the'
            ' return annotation is not a Generator/Iterator/Iterable. (Or it could be'
            ' because the function lacks a return annotation.)',
            'DOC201: Method `StubClass.documentsNothingWithIterator` does not have a'
            ' return section in docstring',
            'DOC403: Method `StubClass.documentsYieldsWithNonGeneratorAnnotation` has a'
            ' "Yields" section in the docstring, but there are no "yield" statements, or'
            ' the return annotation is not a Generator/Iterator/Iterable. (Or it could be'
            ' because the function lacks a return annotation.)',
            'DOC203: Method `StubClass.documentsGeneratorReturnValue` return type(s) in'
            ' docstring not consistent with the return annotation. Return annotation'
            " types: ['Generator[str, None, int]']; docstring return section types:"
            " ['int']",
            'DOC403: Method `StubClass.documentsGeneratorReturnValue` has a "Yields"'
            ' section in the docstring, but there are no "yield" statements, or the'
            ' return annotation is not a Generator/Iterator/Iterable. (Or it could be'
            ' because the function lacks a return annotation.)',
            'DOC403: Method `StubClass.documentsGeneratorReturnValueAsWhole` has a'
            ' "Yields" section in the docstring, but there are no "yield" statements, or'
            ' the return annotation is not a Generator/Iterator/Iterable. (Or it could be'
            ' because the function lacks a return annotation.)',
            'DOC202: Method `StubClass.documentsReturnsWithoutAnnotation` has a return'
            ' section in docstring, but there are no return statements or annotations',
            'DOC203: Method `StubClass.documentsReturnsWithoutAnnotation` return type(s)'
            ' in docstring not consistent with the return annotation. Return annotation'
            ' has 0 type(s); docstring return section has 1 type(s).',
            'DOC105: Method `StubClass.hasWrongArgType`: Argument names match, but type'
            ' hints in these args do not match: var1',
        ],
        '.pyi': [
            'DOC201: Method `StubClass.documentsNothingWithIterator` does not have a'
            ' return section in docstring',
            'DOC403: Method `StubClass.documentsYieldsWithNonGeneratorAnnotation` has a'
            ' "Yields" section in the docstring, but there are no "yield" statements, or'
            ' the return annotation is not a Generator/Iterator/Iterable. (Or it could be'
            ' because the function lacks a return annotation.)',
            'DOC203: Method `StubClass.documentsReturnsWithoutAnnotation` return type(s)'
            ' in docstring not consistent with the return annotation. Return annotation'
            ' has 0 type(s); docstring return section has 1 type(s).',
            'DOC105: Method `StubClass.hasWrongArgType`: Argument names match, but type'
            ' hints in these args do not match: var1',
        ],
    }
    assert list(map(str, violations)) == expectedLookup[suffix]


# These fixtures enable checkArgDefaults=True, which Visitor.__init__ rejects
# for Sphinx style. Only NumPy and Google can exercise default comparison;
# testStubFile covers Sphinx stub-body behavior and argument types instead.
@pytest.mark.parametrize('suffix', ['.py', '.pyi'])
@pytest.mark.parametrize('style', ['google', 'numpy'])
def testStubFileArgDefaults(tmp_path: Path, style: str, suffix: str) -> None:
    """
    Test that, with ``--check-arg-defaults``, a ``...`` default in a stub
    (.pyi) file is treated as a placeholder: the docstring can give any default
    value or none, and only the type is compared.

    As in testStubFile(), the same fixture is checked as a .py file and as a
    .pyi file. In the .py file, ``...`` is a real default value, so docstrings
    that don't say ``default=...`` get DOC105 (arguments) or DOC605 (class
    attributes). In the .pyi file, only wrong types are reported. The fixture
    covers function arguments, class attributes, types whose own text contains
    ``default=``, types wrapped in backticks, and positional-only arguments.
    """
    filename = tmp_path / f'defaults{suffix}'
    shutil.copyfile(DATA_DIR / f'{style}/stub_file/defaults.pyi', filename)
    violations = _checkFile(
        filename=filename,
        style=style,
        checkArgDefaults=True,
        checkClassAttributes=True,
    )
    expectedLookup = {
        '.py': [
            'DOC605: Class `Config`: Attribute names match, but type hints in these'
            ' attributes do not match: retries, timeout, name  (Please read'
            ' https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to'
            ' correctly document class attributes.)',
            'DOC105: Function `connect`: Argument names match, but type hints in these'
            ' args do not match: port, verbose, label . (Note: docstring arg defaults'
            ' should look like: `, default=XXX`)',
            'DOC605: Class `AnnotationDefaults`: Attribute names match, but type hints'
            ' in these attributes do not match: literal, wrongAnnotated, wrongLiteral,'
            ' customDefault  (Please read'
            ' https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to'
            ' correctly document class attributes.)',
            'DOC105: Function `preserveAnnotationDefaults`: Argument names match, but'
            ' type hints in these args do not match: literal, wrongAnnotated,'
            ' wrongLiteral, customDefault . (Note: docstring arg defaults should look'
            ' like: `, default=XXX`)',
            # `placeholder` (documented as ``int, default=...``) matches, but it's
            # still listed: the names in these messages come from a comparison that
            # doesn't remove backticks. This also happens on `main`.
            'DOC605: Class `BacktickDefaults`: Attribute names match, but type hints in'
            ' these attributes do not match: placeholder, customDefault, wrongType'
            '  (Please read'
            ' https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to'
            ' correctly document class attributes.)',
            'DOC105: Function `backtickDefaults`: Argument names match, but type hints in'
            ' these args do not match: placeholder, customDefault, wrongType . (Note:'
            ' docstring arg defaults should look like: `, default=XXX`)',
            'DOC105: Function `positionalOnlyDefaults`: Argument names match, but type'
            ' hints in these args do not match: default . (Note: docstring arg defaults'
            ' should look like: `, default=XXX`)',
        ],
        '.pyi': [
            'DOC605: Class `Config`: Attribute names match, but type hints in these'
            ' attributes do not match: name  (Please read'
            ' https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to'
            ' correctly document class attributes.)',
            'DOC105: Function `connect`: Argument names match, but type hints in these'
            ' args do not match: label . (Note: docstring arg defaults should look'
            ' like: `, default=XXX`)',
            'DOC605: Class `AnnotationDefaults`: Attribute names match, but type hints'
            ' in these attributes do not match: wrongAnnotated, wrongLiteral  (Please'
            ' read https://jsh9.github.io/pydoclint/checking_class_attributes.html on how'
            ' to correctly document class attributes.)',
            'DOC105: Function `preserveAnnotationDefaults`: Argument names match, but'
            ' type hints in these args do not match: wrongAnnotated, wrongLiteral .'
            ' (Note: docstring arg defaults should look like: `, default=XXX`)',
            'DOC605: Class `BacktickDefaults`: Attribute names match, but type hints in'
            ' these attributes do not match: wrongType  (Please read'
            ' https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to'
            ' correctly document class attributes.)',
            'DOC105: Function `backtickDefaults`: Argument names match, but type hints in'
            ' these args do not match: wrongType . (Note: docstring arg defaults should'
            ' look like: `, default=XXX`)',
        ],
    }
    assert list(map(str, violations)) == expectedLookup[suffix]


@pytest.mark.parametrize('style', ['google', 'numpy'])
def testStubFileUntypedArgDefaults(tmp_path: Path, style: str) -> None:
    """
    Like testStubFileArgDefaults(), but for untyped arguments, with both
    type-hint options off: their ``...`` defaults in a stub (.pyi) file can
    also be documented with any default or none.

    Only the .pyi version is tested. As a .py file, the same content gets
    DOC108/DOC111, because default values are treated as type hints
    (https://github.com/jsh9/pydoclint/issues/313), and this test shouldn't
    lock that bug in.
    """
    filename = tmp_path / 'untyped_defaults.pyi'
    shutil.copyfile(
        DATA_DIR / f'{style}/stub_file/untyped_defaults.pyi',
        filename,
    )
    violations = _checkFile(
        filename=filename,
        style=style,
        checkArgDefaults=True,
        argTypeHintsInSignature=False,
        argTypeHintsInDocstring=False,
    )
    assert list(map(str, violations)) == []


@pytest.mark.parametrize('suffix', ['.py', '.pyi'])
def testSphinxRejectsCheckingStubArgDefaults(
        tmp_path: Path,
        suffix: str,
) -> None:
    """
    Test that ``--check-arg-defaults`` with Sphinx style raises an error for
    stub (.pyi) files too, as it does for .py files. (This is why there is no
    Sphinx version of testStubFileArgDefaults().)
    """
    filename = tmp_path / f'cases{suffix}'
    shutil.copyfile(DATA_DIR / 'sphinx/stub_file/cases.pyi', filename)
    with pytest.raises(
        ValueError,
        match=r'--check-arg-defaults is not compatible with --style=sphinx',
    ):
        _checkFile(filename=filename, style='sphinx', checkArgDefaults=True)


@pytest.mark.parametrize(
    ('path', 'includeStubFiles', 'expected'),
    [
        ('pkg', False, ['pkg/a.py', 'pkg/sub/c.py']),
        ('pkg', True, ['pkg/a.py', 'pkg/a.pyi', 'pkg/b.pyi', 'pkg/sub/c.py']),
        # Stub files passed explicitly are always checked
        ('pkg/b.pyi', False, ['pkg/b.pyi']),
    ],
)
def testCheckPathsIncludeStubFiles(
        tmp_path: Path,
        path: str,
        includeStubFiles: bool,
        expected: list[str],
) -> None:
    """
    Test which files a folder scan checks: .py files always, stub (.pyi) files
    only with ``--include-stub-files``, and .pyc files never. The files are
    sorted together, so ``a.pyi`` comes right after ``a.py``. Also test that a
    stub file passed explicitly is checked even when the option is off.
    """
    for name in [
        'a.py',
        'a.pyi',
        'b.pyi',
        'sub/c.py',
        '__pycache__/a.cpython-313.pyc',  # should never be checked
    ]:
        filename = tmp_path / 'pkg' / name
        filename.parent.mkdir(parents=True, exist_ok=True)
        filename.write_text('', encoding='utf-8')

    violations = _checkPaths(
        (str(tmp_path / path),),
        quiet=True,
        # A pattern that matches no file path. (The default, '', would
        # exclude every file, and a pattern such as `\.tox` could match the
        # temporary folder's own path.)
        exclude='^$',
        includeStubFiles=includeStubFiles,
    )
    checkedFiles = [
        Path(_).relative_to(tmp_path).as_posix() for _ in violations
    ]
    assert checkedFiles == expected


@pytest.mark.parametrize('includeStubFiles', [False, True])
def testCheckPathsMatchesExtensionsLikeRglob(
        tmp_path: Path,
        includeStubFiles: bool,
) -> None:
    """
    Test that folder scans match file extensions with the platform's case
    rules, the same way as ``rglob()``: on Windows, ``B.PY`` is a Python file
    and ``E.PYI`` is a stub file; on macOS and Linux, they aren't. Also test
    that every stub file a scan finds is checked as a stub file.
    """
    folder = tmp_path / 'pkg'
    folder.mkdir()
    stubContent = (DATA_DIR / 'numpy/stub_file/cases.pyi').read_text(
        encoding='utf-8',
    )
    for name in [
        'a.py',
        'B.PY',
        'c.Py',
        'd.pyi',
        'E.PYI',
        'f.pyc',
        'G.PYW',
        'h.pyw',
    ]:
        isStub = name.lower().endswith('.pyi')
        (folder / name).write_text(stubContent if isStub else '', 'utf-8')

    violations = _checkPaths(
        (str(folder),),
        quiet=True,
        exclude='^$',  # a pattern that matches no file path
        includeStubFiles=includeStubFiles,
    )
    checkedFiles = [
        Path(_).relative_to(tmp_path).as_posix() for _ in violations
    ]

    patterns = ['*.py', '*.pyi'] if includeStubFiles else ['*.py']
    expected = sorted({_ for p in patterns for _ in folder.rglob(p)})
    assert checkedFiles == [
        _.relative_to(tmp_path).as_posix() for _ in expected
    ]

    # Every stub file that a folder scan finds must also be checked as a stub
    # file: its placeholder bodies must not cause DOC202, DOC403 or DOC502.
    # (DOC201, DOC403 and DOC203 come from methods whose docstrings and return
    # annotations are wrong even without a body.)
    stubFileCodes = {
        Path(name).relative_to(tmp_path).as_posix(): [
            _.fullErrorCode for _ in fileViolations
        ]
        for name, fileViolations in violations.items()
        if Path(name).match('*.pyi')
    }
    for codes in stubFileCodes.values():
        assert codes == ['DOC201', 'DOC403', 'DOC203', 'DOC105']

    if sys.platform == 'win32':
        assert 'pkg/B.PY' in checkedFiles
        assert 'pkg/c.Py' in checkedFiles
        assert ('pkg/E.PYI' in checkedFiles) is includeStubFiles
        assert ('pkg/E.PYI' in stubFileCodes) is includeStubFiles


def testExplicitUppercaseStubFileFollowsPlatformCaseRules(
        tmp_path: Path,
) -> None:
    """
    Test that a stub file passed explicitly follows the platform's case rules,
    like folder scans: ``API.PYI`` is checked as a stub file on Windows, but as
    an ordinary Python file on macOS and Linux.
    """
    # The files go in separate folders, because file names on macOS and
    # Windows ignore case
    results: dict[str, list[str]] = {}
    for folder, name in [
        ('lower', 'api.pyi'),
        ('upper', 'API.PYI'),
        ('python', 'api.py'),
    ]:
        filename = tmp_path / folder / name
        filename.parent.mkdir()
        shutil.copyfile(DATA_DIR / 'numpy/stub_file/cases.pyi', filename)
        violations = _checkFile(filename=filename, style='numpy')
        results[folder] = list(map(str, violations))

    # Make sure that stub files and Python files really get different results
    assert results['lower'] != results['python']

    if sys.platform == 'win32':
        assert results['upper'] == results['lower']
    else:
        assert results['upper'] == results['python']


@pytest.mark.parametrize(
    ('cliOptions', 'pyprojectContent', 'stubFileIsChecked'),
    [
        pytest.param([], None, False, id='default'),
        pytest.param(
            ['--include-stub-files=True'],
            None,
            True,
            id='command-line',
        ),
        pytest.param(
            [],
            '[tool.pydoclint]\ninclude-stub-files = true\n',
            True,
            id='pyproject-toml',
        ),
    ],
)
def testIncludeStubFilesOption(
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        cliOptions: list[str],
        pyprojectContent: str | None,
        stubFileIsChecked: bool,
) -> None:
    """
    Test that ``--include-stub-files`` can be turned on from the command line
    or from pyproject.toml, and that folder scans skip stub (.pyi) files by
    default.
    """
    # Run from `tmp_path` so that this repo's pyproject.toml isn't loaded
    monkeypatch.chdir(tmp_path)
    (tmp_path / 'pkg').mkdir()
    shutil.copyfile(
        DATA_DIR / 'numpy/stub_file/cases.pyi',
        tmp_path / 'pkg/cases.pyi',
    )
    if pyprojectContent is not None:
        (tmp_path / 'pyproject.toml').write_text(
            pyprojectContent,
            encoding='utf-8',
        )

    result = CliRunner().invoke(cliMain, [*cliOptions, 'pkg'])

    # The stub file has violations, so it fails the run if it's checked
    assert result.exit_code == (1 if stubFileIsChecked else 0), result.output
    assert ('pkg/cases.pyi' in result.output) is stubFileIsChecked


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

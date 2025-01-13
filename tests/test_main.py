import copy
import itertools
import sys
from pathlib import Path
from typing import Any, Dict, List

import pytest

from pydoclint.main import _checkFile

THIS_DIR = Path(__file__).parent
DATA_DIR = THIS_DIR / 'data'


def pythonVersionBelow310():
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

expectedViolationsLookup: Dict[bool, List[str]] = {
    True: expectedViolations_True,
    False: expectedViolations_False,
}


@pytest.mark.parametrize(
    'style, filename, checkArgOrder',
    list(
        itertools.product(
            ['google', 'numpy', 'sphinx'],
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
    'style, checkClassAttr',
    list(
        itertools.product(
            ['google', 'numpy', 'sphinx'],
            [True, False],
        ),
    ),
)
def testClassAttributes(
        style: str,
        checkClassAttr: bool,
) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/class_attributes/cases.py',
        checkClassAttributes=checkClassAttr,
        style=style,
    )

    expectedViolations: Dict[bool, List[str]] = {
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


@pytest.mark.parametrize(
    'style',
    ['google', 'numpy', 'sphinx'],
)
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
    'style, filename',
    list(
        itertools.product(
            ['google', 'numpy', 'sphinx'],
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
    'style, filename',
    list(
        itertools.product(
            ['google', 'numpy', 'sphinx'],
            ['function.py', 'classmethod.py', 'method.py', 'staticmethod.py'],
        ),
    ),
)
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

    expectedViolations: List[str] = [
        'DOC201: Method `MyClass.func11` does not have a return section in docstring',
        'DOC203: Method `MyClass.func11` return type(s) in docstring not consistent '
        'with the return annotation. Return annotation has 1 type(s); docstring '
        'return section has 0 type(s).',
    ]

    expectedViolationsCopy = copy.deepcopy(expectedViolations)
    if filename == 'function.py':
        _tweakViolationMsgForFunctions(expectedViolationsCopy)

    assert list(map(str, violations)) == expectedViolationsCopy


@pytest.mark.parametrize(
    'style, require',
    list(
        itertools.product(
            ['google', 'numpy', 'sphinx'],
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
            'DOC201: Function `func` does not have a return section in docstring',
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
            ['google', 'numpy', 'sphinx'],
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
            'DOC201: Function `func` does not have a return section in docstring',
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
    ['google', 'numpy', 'sphinx'],
)
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


@pytest.mark.parametrize(
    'style',
    ['google', 'numpy', 'sphinx'],
)
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


@pytest.mark.parametrize('style', ['google', 'numpy', 'sphinx'])
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


@pytest.mark.parametrize('style', ['google', 'numpy', 'sphinx'])
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


@pytest.mark.parametrize(
    'style',
    ['google', 'numpy', 'sphinx'],
)
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
    ]
    assert list(map(str, violations)) == expected


@pytest.mark.parametrize(
    'style, skipRaisesCheck',
    itertools.product(
        ['google', 'numpy', 'sphinx'],
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
        'DOC501: Function `inner9a` has "raise" statements, but the docstring does '
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
    expected1 = []
    expected = expected1 if skipRaisesCheck else expected0
    assert list(map(str, violations)) == expected


@pytest.mark.parametrize(
    'style, skipRaisesCheck',
    itertools.product(
        ['google', 'numpy', 'sphinx'],
        [False, True],
    ),
)
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
        'DOC501: Method `B.func10` has "raise" statements, but the docstring does not '
        'have a "Raises" section',
        'DOC503: Method `B.func10` exceptions in the "Raises" section in the '
        'docstring do not match those in the function body. Raised exceptions in the '
        "docstring: []. Raised exceptions in the body: ['ValueError'].",
    ]
    expected1 = []
    expected = expected1 if skipRaisesCheck else expected0
    assert list(map(str, violations)) == expected


@pytest.mark.parametrize('style', ['google', 'numpy', 'sphinx'])
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


@pytest.mark.parametrize('style', ['google', 'numpy', 'sphinx'])
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
        checkStyleMismatch=True,
    )
    expected = [
        'DOC001: Class `A`: Potential formatting errors in docstring. Error message: '
        "Expected a colon in 'arg1'.",
        'DOC001: Function/method `__init__`: Potential formatting errors in '
        "docstring. Error message: Expected a colon in 'arg1'. (Note: DOC001 could "
        'trigger other unrelated violations under this function/method too. Please '
        'fix the docstring formatting first.)',
        'DOC003: Function/method `__init__`: Docstring style mismatch. (Please read '
        'more at https://jsh9.github.io/pydoclint/style_mismatch.html ). You '
        'specified "google" style, but the docstring is likely not written in this '
        'style.',
    ]
    assert list(map(str, violations)) == expected


def testParsingErrors_sphinx() -> None:
    violations = _checkFile(
        filename=DATA_DIR / 'sphinx/parsing_errors/cases.py',
        style='sphinx',
        checkStyleMismatch=True,
    )
    expected = []  # not sure how to craft docstrings with parsing errors yet
    assert list(map(str, violations)) == expected


def testParsingErrors_numpy() -> None:
    violations = _checkFile(
        filename=DATA_DIR / 'numpy/parsing_errors/cases.py',
        argTypeHintsInDocstring=False,
        argTypeHintsInSignature=False,
        style='numpy',
        checkStyleMismatch=True,
    )
    expected = [
        'DOC001: Class `A`: Potential formatting errors in docstring. Error message: '
        "Section 'Parameters' is not empty but nothing was parsed.",
        'DOC001: Function/method `__init__`: Potential formatting errors in '
        "docstring. Error message: Section 'Parameters' is not empty but nothing was "
        'parsed. (Note: DOC001 could trigger other unrelated violations under this '
        'function/method too. Please fix the docstring formatting first.)',
        'DOC003: Function/method `__init__`: Docstring style mismatch. (Please read '
        'more at https://jsh9.github.io/pydoclint/style_mismatch.html ). You '
        'specified "numpy" style, but the docstring is likely not written in this '
        'style.',
        'DOC001: Function/method `method2`: Potential formatting errors in docstring. '
        "Error message: Section 'Yields' is not empty but nothing was parsed. (Note: "
        'DOC001 could trigger other unrelated violations under this function/method '
        'too. Please fix the docstring formatting first.)',
        'DOC003: Function/method `method2`: Docstring style mismatch. (Please read '
        'more at https://jsh9.github.io/pydoclint/style_mismatch.html ). You '
        'specified "numpy" style, but the docstring is likely not written in this '
        'style.',
        'DOC101: Method `A.method2`: Docstring contains fewer arguments than in '
        'function signature.',
        'DOC103: Method `A.method2`: Docstring arguments are different from function '
        'arguments. (Or could be other formatting issues: '
        'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
        'Arguments in the function signature but not in the docstring: [arg4: ].',
    ]
    assert list(map(str, violations)) == expected


@pytest.mark.parametrize(
    'expectedStyle, expectedViolations',
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


@pytest.mark.parametrize(
    'style, rrs',
    itertools.product(
        ['google', 'numpy', 'sphinx'],
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
    assert list(map(str, violations)) == expected_lookup[rrs]


@pytest.mark.parametrize(
    'style, rys',
    itertools.product(
        ['google', 'numpy', 'sphinx'],
        [False, True],
    ),
)
def testNoYieldSection(style: str, rys: bool) -> None:
    violations = _checkFile(
        filename=DATA_DIR / f'{style}/no_yield_section/cases.py',
        style=style,
        requireYieldSectionWhenYieldingNothing=rys,
    )
    expected_lookup = {
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
    assert list(map(str, violations)) == expected_lookup[rys]


@pytest.mark.parametrize(
    'style',
    ['google', 'numpy', 'sphinx'],
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
        ['google', 'numpy', 'sphinx'],
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


@pytest.mark.parametrize('style', ['google', 'numpy', 'sphinx'])
def testNoReturnSectionInPropertyMethod(style: str) -> None:
    violations = _checkFile(
        filename=DATA_DIR / 'common/property_method.py',
        style=style,
        skipCheckingShortDocstrings=False,
        checkClassAttributes=False,
    )
    assert len(violations) == 0


@pytest.mark.parametrize(
    'style, argTypeHintsInDocstring, argTypeHintsInSignature',
    itertools.product(
        ['google', 'numpy', 'sphinx'],
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
        ('01/case.py', {'style': 'sphinx'}, []),
        (
            '02/syntax_error_in_type_hints.py',
            {'style': 'numpy'},
            [
                'DOC106: Function `func1`: The option `--arg-type-hints-in-signature` is '
                '`True` but there are no argument type hints in the signature',
                'DOC107: Function `func1`: The option `--arg-type-hints-in-signature` is '
                '`True` but not all args in the signature have type hints',
                'DOC105: Function `func1`: Argument names match, but type hints in these args '
                'do not match: a',
                'DOC106: Function `func2`: The option `--arg-type-hints-in-signature` is '
                '`True` but there are no argument type hints in the signature',
                'DOC107: Function `func2`: The option `--arg-type-hints-in-signature` is '
                '`True` but not all args in the signature have type hints',
                'DOC105: Function `func2`: Argument names match, but type hints in these args '
                'do not match: a',
                'DOC106: Function `func3`: The option `--arg-type-hints-in-signature` is '
                '`True` but there are no argument type hints in the signature',
                'DOC107: Function `func3`: The option `--arg-type-hints-in-signature` is '
                '`True` but not all args in the signature have type hints',
                'DOC105: Function `func3`: Argument names match, but type hints in these args '
                'do not match: a',
            ],
        ),
        (
            '03/union_return_type.py',
            {'style': 'google'},
            [
                'DOC203: Function `myFunc` return type(s) in docstring not consistent with '
                "the return annotation. Return annotation types: ['str | bool | None']; "
                "docstring return section types: ['str | bool | float']"
            ],
        ),
        ('04_backticks/google.py', {'style': 'google'}, []),
        ('04_backticks/numpy.py', {'style': 'numpy'}, []),
        ('04_backticks/numpy.py', {'style': 'numpy'}, []),
        ('05_escape_char/google.py', {'style': 'google'}, []),
        ('05_escape_char/numpy.py', {'style': 'numpy'}, []),
        ('05_escape_char/sphinx.py', {'style': 'sphinx'}, []),
        (
            '06_no_type_hints_in_doc/numpy.py',
            {'style': 'numpy', 'argTypeHintsInDocstring': False},
            [
                'DOC101: Function `f`: Docstring contains fewer arguments than in function '
                'signature.',
                'DOC103: Function `f`: Docstring arguments are different from function '
                'arguments. (Or could be other formatting issues: '
                'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
                'Arguments in the function signature but not in the docstring: [x: int].',
            ],
        ),
        ('07_underscore_args/google.py', {'style': 'google'}, []),
        ('07_underscore_args/numpy.py', {'style': 'numpy'}, []),
        ('07_underscore_args/sphinx.py', {'style': 'sphinx'}, []),
        (
            '07_underscore_args/google_with_violations.py',
            {'style': 'google'},
            [
                'DOC101: Function `foo`: Docstring contains fewer arguments than in function '
                'signature.',
                'DOC103: Function `foo`: Docstring arguments are different from function '
                'arguments. (Or could be other formatting issues: '
                'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
                'Arguments in the function signature but not in the docstring: [c: list].',
            ],
        ),
        ('08_return_section_parsing/google.py', {'style': 'google'}, []),
        ('09_double_quotes_in_Literal/google.py', {'style': 'google'}, []),
        ('09_double_quotes_in_Literal/numpy.py', {'style': 'numpy'}, []),
        (
            '10_absent_return_anno/numpy.py',
            {'style': 'numpy'},
            [
                'DOC403: Function `f1` has a "Yields" section in the docstring, but there are '
                'no "yield" statements, or the return annotation is not a '
                'Generator/Iterator/Iterable. (Or it could be because the function lacks a '
                'return annotation.)',
                'DOC404: Function `f1` yield type(s) in docstring not consistent with the '
                'return annotation. Return annotation does not exist or is not '
                'Generator[...]/Iterator[...]/Iterable[...], but docstring "yields" section '
                'has 1 type(s).',
            ],
        ),
        (
            '11_private_class_attr/google.py',
            {'style': 'google', 'shouldDocumentPrivateClassAttributes': False},
            [],
        ),
        (
            '11_private_class_attr/google.py',
            {'style': 'google', 'shouldDocumentPrivateClassAttributes': True},
            [
                'DOC601: Class `MyClass`: Class docstring contains fewer class attributes '
                'than actual class attributes.  (Please read '
                'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
                'correctly document class attributes.)',
                'DOC603: Class `MyClass`: Class docstring attributes are different from '
                'actual class attributes. (Or could be other formatting issues: '
                'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
                'Attributes in the class definition but not in the docstring: [_hidden_attr: '
                'bool]. (Please read '
                'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
                'correctly document class attributes.)',
            ],
        ),
        (
            '12_property_methods_as_class_attr/google.py',
            {
                'style': 'google',
                'checkClassAttributes': True,
                'treatPropertyMethodsAsClassAttributes': True,
                'shouldDocumentPrivateClassAttributes': True,
            },
            [],
        ),
        (
            '12_property_methods_as_class_attr/google.py',
            {
                'style': 'google',
                'checkClassAttributes': True,
                'treatPropertyMethodsAsClassAttributes': True,
                'shouldDocumentPrivateClassAttributes': False,
            },
            [
                'DOC602: Class `House`: Class docstring contains more class attributes than '
                'in actual class attributes.  (Please read '
                'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
                'correctly document class attributes.)',
                'DOC603: Class `House`: Class docstring attributes are different from actual '
                'class attributes. (Or could be other formatting issues: '
                'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
                'Arguments in the docstring but not in the actual class attributes: '
                '[_privateProperty: str]. (Please read '
                'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
                'correctly document class attributes.)',
            ],
        ),
        (
            '12_property_methods_as_class_attr/google.py',
            {
                'style': 'google',
                'checkClassAttributes': True,
                'treatPropertyMethodsAsClassAttributes': False,
                'shouldDocumentPrivateClassAttributes': True,
            },
            [
                'DOC602: Class `House`: Class docstring contains more class attributes than '
                'in actual class attributes.  (Please read '
                'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
                'correctly document class attributes.)',
                'DOC603: Class `House`: Class docstring attributes are different from actual '
                'class attributes. (Or could be other formatting issues: '
                'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
                'Arguments in the docstring but not in the actual class attributes: '
                '[_privateProperty: str, price: float]. (Please read '
                'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
                'correctly document class attributes.)',
            ],
        ),
        (
            '12_property_methods_as_class_attr/google.py',
            {
                'style': 'google',
                'checkClassAttributes': True,
                'treatPropertyMethodsAsClassAttributes': False,
                'shouldDocumentPrivateClassAttributes': False,
            },
            [
                'DOC602: Class `House`: Class docstring contains more class attributes than '
                'in actual class attributes.  (Please read '
                'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
                'correctly document class attributes.)',
                'DOC603: Class `House`: Class docstring attributes are different from actual '
                'class attributes. (Or could be other formatting issues: '
                'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
                'Arguments in the docstring but not in the actual class attributes: '
                '[_privateProperty: str, price: float]. (Please read '
                'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
                'correctly document class attributes.)',
            ],
        ),
        (
            '13_class_attr_assignments/google.py',
            {
                'style': 'google',
                'checkClassAttributes': True,
            },
            [],
        ),
        (
            '14_folders_ending_in_py.py',  # This is actually a folder
            {},
            [],  # Here we ensure that pydoclint doesn't treat this as a file
        ),
        (
            # Here we ensure that Python files under such folders (whose
            # names end in `.py`) can still get recognized and checked.
            '14_folders_ending_in_py.py/google.py',
            {'style': 'google'},
            [
                'DOC105: Function `function1`: Argument names match, but type hints in these '
                'args do not match: arg1'
            ],
        ),
        ('15_very_long_annotations/sphinx.py', {'style': 'sphinx'}, []),
        ('15_very_long_annotations/google.py', {'style': 'google'}, []),
        ('15_very_long_annotations/numpy.py', {'style': 'numpy'}, []),
        ('16_assign_to_attr/cases.py', {'style': 'sphinx'}, []),
        ('16_assign_to_attr/cases.py', {'style': 'google'}, []),
        ('16_assign_to_attr/cases.py', {'style': 'numpy'}, []),
        (
            '17_ClassVar/cases.py',
            {
                'style': 'google',
                'checkClassAttributes': True,
                'onlyAttrsWithClassVarAreTreatedAsClassAttrs': False,
            },
            [
                'DOC601: Class `AttrsClass`: Class docstring contains fewer class attributes '
                'than actual class attributes.  (Please read '
                'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
                'correctly document class attributes.)',
                'DOC603: Class `AttrsClass`: Class docstring attributes are different from '
                'actual class attributes. (Or could be other formatting issues: '
                'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
                'Attributes in the class definition but not in the docstring: [b: int, d: '
                'str]. (Please read '
                'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
                'correctly document class attributes.)',
                'DOC601: Class `DataClass`: Class docstring contains fewer class attributes '
                'than actual class attributes.  (Please read '
                'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
                'correctly document class attributes.)',
                'DOC603: Class `DataClass`: Class docstring attributes are different from '
                'actual class attributes. (Or could be other formatting issues: '
                'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
                'Attributes in the class definition but not in the docstring: [f: int, g: '
                'float, h: str]. (Please read '
                'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
                'correctly document class attributes.)',
                'DOC601: Class `PydanticClass`: Class docstring contains fewer class '
                'attributes than actual class attributes.  (Please read '
                'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
                'correctly document class attributes.)',
                'DOC603: Class `PydanticClass`: Class docstring attributes are different from '
                'actual class attributes. (Or could be other formatting issues: '
                'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
                'Attributes in the class definition but not in the docstring: [j: int, k: '
                'float, l: str]. (Please read '
                'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
                'correctly document class attributes.)',
            ],
        ),
        (
            '17_ClassVar/cases.py',
            {
                'style': 'google',
                'checkClassAttributes': True,
                'onlyAttrsWithClassVarAreTreatedAsClassAttrs': True,
            },
            [
                'DOC602: Class `AttrsClass`: Class docstring contains more class attributes '
                'than in actual class attributes.  (Please read '
                'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
                'correctly document class attributes.)',
                'DOC603: Class `AttrsClass`: Class docstring attributes are different from '
                'actual class attributes. (Or could be other formatting issues: '
                'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
                'Arguments in the docstring but not in the actual class attributes: [c: '
                'float]. (Please read '
                'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
                'correctly document class attributes.)',
                'DOC605: Class `DataClass`: Attribute names match, but type hints in these '
                'attributes do not match: e  (Please read '
                'https://jsh9.github.io/pydoclint/checking_class_attributes.html on how to '
                'correctly document class attributes.)',
            ],
        ),
        ('18_assign_to_subscript/case.py', {}, []),
        ('19_file_encoding/nonascii.py', {}, []),  # from: https://github.com/ipython/ipython/blob/0334d9f71e7a97394a73c15c663ca50d65df62e1/IPython/core/tests/nonascii.py
        ('19_file_encoding/nonascii2.py', {}, []),  # from: https://github.com/ipython/ipython/blob/0334d9f71e7a97394a73c15c663ca50d65df62e1/IPython/core/tests/nonascii2.py
        ('20_invisible_zero_width_chars/case.py', {}, []),
        (
            '21_syntax_error/case_21a.py',
            {},
            [
                'DOC002: Syntax errors; cannot parse'  # noqa: ISC003
                + ' this Python file. Error message: '
                + (
                    'unterminated string literal (detected at line 4)'
                    if sys.version_info >= (3, 10)
                    else 'invalid syntax'
                )
                + ' (<unknown>, line {num})'.format(
                    num=1 if sys.version_info < (3, 10) else 4
                )
            ],
        ),
        (
            '21_syntax_error/case_21b.py',
            {},
            [
                'DOC002: Syntax errors; cannot parse'  # noqa: ISC003
                + ' this Python file. Error message: Missing '
                + "parentheses in call to 'print'."
                + ' Did you mean print({foo})?'.format(
                    foo="'haha'" if sys.version_info < (3, 10) else '...'
                )
                + ' (<unknown>, line 2)'
            ],
        ),
        (
            '21_syntax_error/case_21c.py',
            {},
            [
                'DOC002: Syntax errors; cannot parse'  # noqa: ISC003
                + ' this Python file. Error message: Missing '
                + "parentheses in call to 'print'."
                + ' Did you mean print({foo})?'.format(
                    foo='"BOM BOOM!"' if sys.version_info < (3, 10) else '...'
                )
                + ' (<unknown>, line 2)'
            ],
        ),
        (
            '22_PEP696_generator/case.py',
            {'style': 'numpy'},
            [],
        ),
        (
            '23_bare_return_stmt_with_yield/google.py',
            {
                'style': 'google',
                'argTypeHintsInDocstring': False,
                'checkYieldTypes': False,
                'checkReturnTypes': True,
            },
            [
                'DOC203: Function `my_func_2` return type(s) in docstring not consistent with '
                "the return annotation. Return annotation types: ['None']; docstring return "
                "section types: ['']"
            ],
        ),
        (
            '23_bare_return_stmt_with_yield/google.py',
            {
                'style': 'google',
                'argTypeHintsInDocstring': False,
                'checkYieldTypes': False,
                'checkReturnTypes': False,
            },
            [],
        ),
        (
            '23_bare_return_stmt_with_yield/google.py',
            {
                'style': 'google',
                'argTypeHintsInDocstring': False,
                'checkYieldTypes': True,
                'checkReturnTypes': True,
            },
            [
                'DOC404: Function `my_func_1` yield type(s) in docstring not consistent with '
                'the return annotation. The yield type (the 0th arg in '
                'Generator[...]/Iterator[...]): int; docstring "yields" section types:',
                'DOC203: Function `my_func_2` return type(s) in docstring not consistent with '
                "the return annotation. Return annotation types: ['None']; docstring return "
                "section types: ['']",
            ],
        ),
        (
            '23_bare_return_stmt_with_yield/google.py',
            {
                'style': 'google',
                'argTypeHintsInDocstring': False,
                'checkYieldTypes': True,
                'checkReturnTypes': False,
            },
            [
                'DOC404: Function `my_func_1` yield type(s) in docstring not consistent with '
                'the return annotation. The yield type (the 0th arg in '
                'Generator[...]/Iterator[...]): int; docstring "yields" section types:',
            ],
        ),
        (
            '24_star_arguments/numpy.py',
            {'style': 'numpy', 'shouldDocumentStarArguments': True},
            [
                'DOC101: Function `function_1`: Docstring contains fewer arguments than in '
                'function signature.',
                'DOC103: Function `function_1`: Docstring arguments are different from '
                'function arguments. (Or could be other formatting issues: '
                'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
                'Arguments in the function signature but not in the docstring: [**kwargs: '
                'Any, *args: Any].',
                'DOC101: Function `function_3`: Docstring contains fewer arguments than in '
                'function signature.',
                'DOC103: Function `function_3`: Docstring arguments are different from '
                'function arguments. (Or could be other formatting issues: '
                'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
                'Arguments in the function signature but not in the docstring: [*args: Any].',
            ],
        ),
        (
            '24_star_arguments/numpy.py',
            {'style': 'numpy', 'shouldDocumentStarArguments': False},
            [
                'DOC102: Function `function_2`: Docstring contains more arguments than in '
                'function signature.',
                'DOC103: Function `function_2`: Docstring arguments are different from '
                'function arguments. (Or could be other formatting issues: '
                'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
                'Arguments in the docstring but not in the function signature: [**kwargs: '
                'Any, *args: Any].',
                'DOC102: Function `function_3`: Docstring contains more arguments than in '
                'function signature.',
                'DOC103: Function `function_3`: Docstring arguments are different from '
                'function arguments. (Or could be other formatting issues: '
                'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
                'Arguments in the docstring but not in the function signature: [**kwargs: Any].',
            ],
        ),
    ],
)
def testEdgeCases(
        filename: str,
        options: Dict[str, Any],
        expectedViolations: List[str],
) -> None:
    fullFilename: Path = DATA_DIR / 'edge_cases' / filename

    if not fullFilename.is_file() and filename != '14_folders_ending_in_py.py':
        raise FileNotFoundError('The file you want to test does not exist')

    violations = _checkFile(filename=fullFilename, **options)
    assert list(map(str, violations)) == expectedViolations


def testPlayground() -> None:
    """
    This is a placeholder test for testing the `playground.py` file.

    When you want to quickly test something, you can add contents into
    tests/data/playground.py and run this test function.
    """
    violations = _checkFile(
        filename=DATA_DIR / 'playground.py',
        style='numpy',
    )
    expected = []
    assert list(map(str, violations)) == expected

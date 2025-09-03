import sys
from pathlib import Path
from typing import Any, Dict, List

import pytest

from pydoclint.main import _checkFile
from tests.test_main import DATA_DIR


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
        ('09_double_quotes/google.py', {'style': 'google'}, []),
        ('09_double_quotes/numpy.py', {'style': 'numpy'}, []),
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
        (
            '19_file_encoding/nonascii.py',
            {},
            [],
        ),  # from: https://github.com/ipython/ipython/blob/0334d9f71e7a97394a73c15c663ca50d65df62e1/IPython/core/tests/nonascii.py
        (
            '19_file_encoding/nonascii2.py',
            {},
            [],
        ),  # from: https://github.com/ipython/ipython/blob/0334d9f71e7a97394a73c15c663ca50d65df62e1/IPython/core/tests/nonascii2.py
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
        (
            '25_underscore_and_private_args/cases.py',
            {
                'style': 'google',
                'ignoreUnderscoreArgs': False,
                'argTypeHintsInDocstring': False,
            },
            [
                'DOC101: Function `function_1`: Docstring contains fewer arguments than in '
                'function signature.',
                'DOC103: Function `function_1`: Docstring arguments are different from '
                'function arguments. (Or could be other formatting issues: '
                'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
                'Arguments in the function signature but not in the docstring: [_: float, __: '
                'bool, __d: list, _c: dict].',
            ],
        ),
        (
            '25_underscore_and_private_args/cases.py',
            {
                'style': 'google',
                'ignoreUnderscoreArgs': False,
                'ignorePrivateArgs': True,
                'argTypeHintsInDocstring': False,
            },
            [
                'DOC101: Function `function_1`: Docstring contains fewer arguments than in '
                'function signature.',
                'DOC103: Function `function_1`: Docstring arguments are different from '
                'function arguments. (Or could be other formatting issues: '
                'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
                'Arguments in the function signature but not in the docstring: [_: float, __: '
                'bool].',
            ],
        ),
        (
            '25_underscore_and_private_args/cases.py',
            {
                'style': 'google',
                'argTypeHintsInDocstring': False,
            },
            [
                'DOC101: Function `function_1`: Docstring contains fewer arguments than in '
                'function signature.',
                'DOC103: Function `function_1`: Docstring arguments are different from '
                'function arguments. (Or could be other formatting issues: '
                'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
                'Arguments in the function signature but not in the docstring: [__d: list, '
                '_c: dict].',
            ],
        ),
        (
            '25_underscore_and_private_args/cases.py',
            {
                'style': 'google',
                'ignorePrivateArgs': True,
                'argTypeHintsInDocstring': False,
            },
            [],
        ),
        ('26_decompose_tuples/cases.py', {}, []),
        ('27_declare_assert_error/cases.py', {'style': 'google'}, []),
        (
            '28_numpy_style_detection/case.py',
            {
                'style': 'numpy',
                'checkStyleMismatch': True,
            },
            [
                'DOC101: Function `funcWithReturnsSection`: Docstring contains fewer '
                'arguments than in function signature.',
                'DOC103: Function `funcWithReturnsSection`: Docstring arguments are different '
                'from function arguments. (Or could be other formatting issues: '
                'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
                'Arguments in the function signature but not in the docstring: [arg1: str].',
                'DOC003: Function/method `funcWithoutNumpyDashes`: Docstring style mismatch. '
                '(Please read more at https://jsh9.github.io/pydoclint/style_mismatch.html ). '
                'You specified "numpy" style, but the docstring is likely not written in this '
                'style.',
            ],
        ),
        (
            '28_numpy_style_detection/case.py',
            {
                'style': 'google',
                'checkStyleMismatch': True,
            },
            [
                'DOC003: Function/method `add1`: Docstring style mismatch. '
                '(Please read more at https://jsh9.github.io/pydoclint/style_mismatch.html ). '
                'You specified "google" style, but the docstring is likely not written in '
                'this style.',
                'DOC003: Function/method `add2`: Docstring style mismatch. '
                '(Please read more at https://jsh9.github.io/pydoclint/style_mismatch.html ). '
                'You specified "google" style, but the docstring is likely not written in '
                'this style.',
                'DOC003: Function/method `funcWithReturnsSection`: Docstring style mismatch. '
                '(Please read more at https://jsh9.github.io/pydoclint/style_mismatch.html ). '
                'You specified "google" style, but the docstring is likely not written in '
                'this style.',
                'DOC101: Function `funcWithReturnsSection`: Docstring contains fewer '
                'arguments than in function signature.',
                'DOC103: Function `funcWithReturnsSection`: Docstring arguments are different '
                'from function arguments. (Or could be other formatting issues: '
                'https://jsh9.github.io/pydoclint/violation_codes.html#notes-on-doc103 ). '
                'Arguments in the function signature but not in the docstring: [arg1: str].',
                'DOC003: Function/method `funcWithArgsSection`: Docstring style mismatch. '
                '(Please read more at https://jsh9.github.io/pydoclint/style_mismatch.html ). '
                'You specified "google" style, but the docstring is likely not written in '
                'this style.',
                'DOC003: Function/method `funcWithExamplesSection`: Docstring style mismatch. '
                '(Please read more at https://jsh9.github.io/pydoclint/style_mismatch.html ). '
                'You specified "google" style, but the docstring is likely not written in '
                'this style.',
                'DOC003: Function/method `funcWithNumpyStyleDashes`: Docstring style '
                'mismatch. (Please read more at '
                'https://jsh9.github.io/pydoclint/style_mismatch.html ). You specified '
                '"google" style, but the docstring is likely not written in this style.',
            ],
        ),
        (
            '29_yields_section/case.py',
            {
                'style': 'google',
                'skipCheckingShortDocstrings': True,
            },
            [
                'DOC404: Function `test_yield_with_typing_no_args` yield type(s) in docstring '
                'not consistent with the return annotation. The yield type (the 0th arg in '
                'Generator[...]/Iterator[...]): Generator[typing.Any]; docstring "yields" '
                'section types: Generator123[typing.Any]'
            ],
        ),
        (
            '30_comments_in_type_hints/numpy.py',
            {
                'style': 'numpy',
                'checkClassAttributes': True,
                'checkArgDefaults': True,
            },
            [
                'DOC105: Function `regular_function`: Argument names match, but type hints in '
                'these args do not match: param4 . (Note: docstring arg defaults should look '
                'like: `, default=XXX`)'
            ],
        ),
        (
            '31_syntax_error_in_parsing_type_hints/numpy.py',
            {
                'style': 'numpy',
                'checkArgDefaults': True,
            },
            [],
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

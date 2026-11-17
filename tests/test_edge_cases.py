import sys
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

import pytest

from pydoclint.main import _checkFile
from tests.test_main import DATA_DIR


@pytest.mark.parametrize(
    ('filename', 'options', 'expectedViolations'),
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
            {
                'style': 'google',
                'ignorePrivateClassAttributes': True,
                'ignoreUnderscoreOnlyClassAttributes': True,
                'ignoreSpecialDunderClassAttributes': True,
            },
            [],
        ),
        (
            '11_private_class_attr/google.py',
            {
                'style': 'google',
                'ignorePrivateClassAttributes': False,
                'ignoreUnderscoreOnlyClassAttributes': False,
                'ignoreSpecialDunderClassAttributes': False,
            },
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
                'ignorePrivateClassAttributes': False,
                'ignoreUnderscoreOnlyClassAttributes': False,
                'ignoreSpecialDunderClassAttributes': False,
            },
            [],
        ),
        (
            '12_property_methods_as_class_attr/google.py',
            {
                'style': 'google',
                'checkClassAttributes': True,
                'treatPropertyMethodsAsClassAttributes': True,
                'ignorePrivateClassAttributes': True,
                'ignoreUnderscoreOnlyClassAttributes': True,
                'ignoreSpecialDunderClassAttributes': True,
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
                'ignorePrivateClassAttributes': False,
                'ignoreUnderscoreOnlyClassAttributes': False,
                'ignoreSpecialDunderClassAttributes': False,
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
                'ignorePrivateClassAttributes': True,
                'ignoreUnderscoreOnlyClassAttributes': True,
                'ignoreSpecialDunderClassAttributes': True,
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
                + f' (<unknown>, line {1 if sys.version_info < (3, 10) else 4})'
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
                'Generator[...]/Iterator[...]): typing.Any; docstring "yields" '
                'section types: Generator123[typing.Any]',
                'DOC404: Function `invalid_iterator_extra_arg` yield type(s) in docstring '
                'not consistent with the return annotation. The yield type (the 0th arg in '
                'Generator[...]/Iterator[...]): (int, str); docstring "yields" section '
                'types: int',
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
        (
            '32_multiple_init/allow_init_docstring/google.py',
            {'style': 'google', 'allowInitDocstring': True},
            [],
        ),
        (
            '32_multiple_init/allow_init_docstring/numpy.py',
            {'style': 'numpy', 'allowInitDocstring': True},
            [],
        ),
        (
            '32_multiple_init/allow_init_docstring/sphinx.py',
            {'style': 'sphinx', 'allowInitDocstring': True},
            [],
        ),
        (
            '32_multiple_init/doesnt_allow_init_docstring/google.py',
            {'style': 'google'},
            [],
        ),
        (
            '32_multiple_init/doesnt_allow_init_docstring/numpy.py',
            {'style': 'numpy'},
            [],
        ),
        (
            '32_multiple_init/doesnt_allow_init_docstring/sphinx.py',
            {'style': 'sphinx'},
            [],
        ),
        (
            '33_private_functions/case.py',
            {
                'style': 'google',
                'skipCheckingPrivateFunctions': False,
                'skipCheckingShortDocstrings': False,
            },
            [
                'DOC203: Function `_test_private_function` return type(s) in docstring not '
                "consistent with the return annotation. Return annotation types: ['int']; "
                "docstring return section types: ['bool']",
                'DOC203: Function `_` return type(s) in docstring not consistent with the'
                " return annotation. Return annotation types: ['int']; docstring return"
                " section types: ['bool']",
                'DOC203: Function `__` return type(s) in docstring not consistent with the'
                " return annotation. Return annotation types: ['int']; docstring return"
                " section types: ['bool']",
                'DOC203: Function `inner_function` return type(s) in docstring not'
                " consistent with the return annotation. Return annotation types: ['bool'];"
                " docstring return section types: ['int']",
                'DOC203: Function `__special__` return type(s) in docstring not consistent'
                " with the return annotation. Return annotation types: ['int']; docstring"
                " return section types: ['bool']",
                'DOC301: Class `TestClass`: __init__() should not have a docstring; '
                'please combine it with the docstring of the class',
                'DOC105: Method `TestClass._private_method`: Argument names match, but type '
                'hints in these args do not match: i',
                'DOC203: Function `inner_method` return type(s) in docstring not consistent '
                "with the return annotation. Return annotation types: ['bool']; docstring "
                "return section types: ['int']",
                'DOC105: Method `TestClass.__private_name_mangled_method`: Argument names '
                'match, but type hints in these args do not match: i',
            ],
        ),
        (
            '33_private_functions/case.py',
            {
                'style': 'google',
                'skipCheckingPrivateFunctions': True,
                'skipCheckingShortDocstrings': False,
            },
            [
                'DOC203: Function `__special__` return type(s) in docstring not consistent'
                " with the return annotation. Return annotation types: ['int']; docstring"
                " return section types: ['bool']",
                'DOC301: Class `TestClass`: __init__() should not have a docstring; '
                'please combine it with the docstring of the class',
            ],
        ),
        (
            '35_doc404_return_and_yield_double_unwrap/google.py',
            {
                'style': 'google',
                'argTypeHintsInDocstring': False,
                'checkYieldTypes': True,
                'checkReturnTypes': True,
            },
            [
                'DOC404: Function `iteratorDictMismatch` yield type(s) in docstring '
                'not consistent with the return annotation. The yield type (the 0th '
                'arg in Generator[...]/Iterator[...]): Dict[str, Any]; docstring '
                '"yields" section types: str'
            ],
        ),
        (
            '35_doc404_return_and_yield_double_unwrap/numpy.py',
            {
                'style': 'numpy',
                'checkYieldTypes': True,
                'checkReturnTypes': True,
            },
            [
                'DOC404: Function `iteratorDictMismatch` yield type(s) in docstring '
                'not consistent with the return annotation. The yield type (the 0th '
                'arg in Generator[...]/Iterator[...]): Dict[str, Any]; docstring '
                '"yields" section types: str'
            ],
        ),
        (
            '35_doc404_return_and_yield_double_unwrap/sphinx.py',
            {
                'style': 'sphinx',
                'checkYieldTypes': True,
                'checkReturnTypes': True,
            },
            [
                'DOC404: Function `iteratorDictMismatch` yield type(s) in docstring '
                'not consistent with the return annotation. The yield type (the 0th '
                'arg in Generator[...]/Iterator[...]): Dict[str, Any]; docstring '
                '"yields" section types: str'
            ],
        ),
        (
            '36_underscore_only_class_attribute/case.py',
            {
                'style': 'numpy',
                'argTypeHintsInDocstring': False,
                'checkClassAttributes': True,
                'ignorePrivateClassAttributes': False,
                'ignoreUnderscoreOnlyClassAttributes': True,
            },
            [],
        ),
    ],
)
def testEdgeCases(
        filename: str,
        options: dict[str, Any],
        expectedViolations: list[str],
) -> None:
    fullFilename: Path = DATA_DIR / 'edge_cases' / filename

    if not fullFilename.is_file() and filename != '14_folders_ending_in_py.py':
        raise FileNotFoundError('The file you want to test does not exist')

    violations = _checkFile(filename=fullFilename, **options)
    assert list(map(str, violations)) == expectedViolations


@pytest.mark.parametrize('style', ['google', 'numpy'])
@pytest.mark.parametrize(
    ('fixture', 'options', 'expectedViolations'),
    [
        pytest.param(
            'default_only',
            {'checkArgDefaults': True},
            [
                # DOC106/DOC107: type hints are required in the signature, but
                # `value` has none (its default doesn't count as one)
                'DOC106: Function `f`: The option `--arg-type-hints-in-signature`'
                ' is `True` but there are no argument type hints in the'
                ' signature',
                'DOC107: Function `f`: The option `--arg-type-hints-in-signature`'
                ' is `True` but not all args in the signature have type hints',
                # DOC109/DOC110: the same, for the docstring
                'DOC109: Function `f`: The option `--arg-type-hints-in-docstring`'
                ' is `True` but there are no type hints in the docstring arg'
                ' list',
                'DOC110: Function `f`: The option `--arg-type-hints-in-docstring`'
                ' is `True` but not all args in the docstring arg list have type'
                ' hints',
            ],
            id='type-hints-required',
        ),
        pytest.param(
            'default_only',
            {
                'checkArgDefaults': True,
                'argTypeHintsInSignature': False,
                'argTypeHintsInDocstring': False,
            },
            # No DOC108/DOC111 ("there are type hints, but there shouldn't
            # be"): the defaults aren't type hints
            [],
            id='type-hints-not-allowed',
        ),
        pytest.param(
            'default_only',
            {'checkArgDefaults': False},
            [
                'DOC106: Function `f`: The option `--arg-type-hints-in-signature`'
                ' is `True` but there are no argument type hints in the'
                ' signature',
                'DOC107: Function `f`: The option `--arg-type-hints-in-signature`'
                ' is `True` but not all args in the signature have type hints',
                'DOC109: Function `f`: The option `--arg-type-hints-in-docstring`'
                ' is `True` but there are no type hints in the docstring arg'
                ' list',
                'DOC110: Function `f`: The option `--arg-type-hints-in-docstring`'
                ' is `True` but not all args in the docstring arg list have type'
                ' hints',
                # DOC105: with both type-hint options on, pydoclint compares the
                # type hint text of `value` in the signature and the docstring.
                # Without --check-arg-defaults, the signature's default isn't
                # added to that text, so it is '' (no type), while the
                # docstring's is ', default=3'. They differ, so DOC105 reports
                # it: without --check-arg-defaults, docstrings shouldn't give
                # defaults (see docs/style_deviations.md). (In the first case,
                # with --check-arg-defaults, both are ', default=3'.)
                'DOC105: Function `f`: Argument names match, but type hints in'
                ' these args do not match: value',
            ],
            id='type-hints-required-defaults-not-checked',
        ),
        pytest.param(
            'partly_typed',
            {'checkArgDefaults': True},
            [
                # Only DOC107/DOC110 ("not all args have type hints"), because
                # `count` has a type hint and `value` doesn't
                'DOC107: Function `f`: The option `--arg-type-hints-in-signature`'
                ' is `True` but not all args in the signature have type hints',
                'DOC110: Function `f`: The option `--arg-type-hints-in-docstring`'
                ' is `True` but not all args in the docstring arg list have type'
                ' hints',
            ],
            id='some-args-typed',
        ),
    ],
)
def testDefaultAloneIsNotATypeHint(
        style: str,
        fixture: str,
        options: dict[str, Any],
        expectedViolations: list[str],
) -> None:
    """
    Test that a default value alone is not a type hint.

    In the fixtures, ``value=3`` has a default but no type annotation. The
    numpy docstrings document it as ``value : , default=3``, and the Google
    ones as ``value (, default=3): ...``. See
    https://github.com/jsh9/pydoclint/issues/313.
    """
    fixtureDir = DATA_DIR / 'edge_cases/37_untyped_arg_defaults' / fixture
    violations = _checkFile(
        filename=fixtureDir / f'{style}.py',
        style=style,
        **options,
    )
    assert list(map(str, violations)) == expectedViolations


@pytest.mark.parametrize('style', ['google', 'numpy'])
@pytest.mark.parametrize(
    ('fixture', 'options', 'expectedViolations'),
    [
        pytest.param(
            'types_only_in_docstring',
            {'checkArgDefaults': True, 'argTypeHintsInSignature': False},
            [
                'DOC105: Function `wrongDefault`: Argument names match, but type'
                ' hints in these args do not match: alpha . (Note: docstring arg'
                ' defaults should look like: `, default=XXX`)',
                'DOC105: Function `missingDefault`: Argument names match, but'
                ' type hints in these args do not match: alpha . (Note:'
                ' docstring arg defaults should look like: `, default=XXX`)',
                'DOC105: Function `spuriousDefault`: Argument names match, but'
                ' type hints in these args do not match: alpha . (Note:'
                ' docstring arg defaults should look like: `, default=XXX`)',
                # The same three cases, after a type that isn't valid Python
                'DOC105: Function `freeFormWrongDefault`: Argument names match, but'
                ' type hints in these args do not match: values . (Note:'
                ' docstring arg defaults should look like: `, default=XXX`)',
                'DOC105: Function `freeFormMissingDefault`: Argument names match, but'
                ' type hints in these args do not match: values . (Note:'
                ' docstring arg defaults should look like: `, default=XXX`)',
                'DOC105: Function `freeFormSpuriousDefault`: Argument names match, but'
                ' type hints in these args do not match: values . (Note:'
                ' docstring arg defaults should look like: `, default=XXX`)',
            ],
            id='types-only-in-docstring',
        ),
        pytest.param(
            'types_only_in_docstring',
            {'checkArgDefaults': False, 'argTypeHintsInSignature': False},
            [],  # without --check-arg-defaults, defaults aren't compared
            id='types-only-in-docstring-defaults-not-checked',
        ),
        pytest.param(
            'types_only_in_signature',
            {'checkArgDefaults': True, 'argTypeHintsInDocstring': False},
            [
                'DOC105: Function `wrongDefault`: Argument names match, but type'
                ' hints in these args do not match: x . (Note: docstring arg'
                ' defaults should look like: `, default=XXX`)',
                'DOC105: Function `missingDefault`: Argument names match, but'
                ' type hints in these args do not match: x . (Note:'
                ' docstring arg defaults should look like: `, default=XXX`)',
                'DOC105: Function `spuriousDefault`: Argument names match, but'
                ' type hints in these args do not match: x . (Note:'
                ' docstring arg defaults should look like: `, default=XXX`)',
            ],
            id='types-only-in-signature',
        ),
        pytest.param(
            'no_types',
            {
                'checkArgDefaults': True,
                'argTypeHintsInSignature': False,
                'argTypeHintsInDocstring': False,
            },
            [
                'DOC105: Function `wrongDefault`: Argument names match, but type'
                ' hints in these args do not match: value . (Note: docstring arg'
                ' defaults should look like: `, default=XXX`)',
                'DOC105: Function `missingDefault`: Argument names match, but'
                ' type hints in these args do not match: value . (Note:'
                ' docstring arg defaults should look like: `, default=XXX`)',
                'DOC105: Function `spuriousDefault`: Argument names match, but'
                ' type hints in these args do not match: value . (Note:'
                ' docstring arg defaults should look like: `, default=XXX`)',
            ],
            id='no-types',
        ),
    ],
)
def testDefaultsAreComparedWhenTypesAreNot(
        style: str,
        fixture: str,
        options: dict[str, Any],
        expectedViolations: list[str],
) -> None:
    """
    Test that, with ``--check-arg-defaults``, the documented default values are
    compared with the signature even when the type-hint options turn off the
    comparison of types (which needs both options to be True). A wrong,
    missing, or spurious default gets DOC105 (the type hints, which include the
    defaults, don't match). See https://github.com/jsh9/pydoclint/issues/313.
    """
    fixtureDir = DATA_DIR / 'edge_cases/37_untyped_arg_defaults' / fixture
    violations = _checkFile(
        filename=fixtureDir / f'{style}.py',
        style=style,
        **options,
    )
    assert list(map(str, violations)) == expectedViolations


@pytest.mark.parametrize(
    ('fixtureFile', 'options', 'expectedViolations'),
    [
        # `...` in a stub file is a placeholder, so any documented default is
        # fine for `x`, even after a type that isn't valid Python
        pytest.param(
            'stub_placeholders/numpy.pyi',
            {'style': 'numpy'},
            [],
            id='stub-placeholders-numpy',
        ),
        pytest.param(
            'stub_placeholders/google.pyi',
            {'style': 'google'},
            [],
            id='stub-placeholders-google',
        ),
        # Class attribute defaults are only compared together with the types
        # (both type-hint options on), so the wrong default isn't reported
        pytest.param(
            'class_attributes/numpy.py',
            {'style': 'numpy', 'checkClassAttributes': True},
            [],
            id='class-attributes-numpy',
        ),
        pytest.param(
            'class_attributes/google.py',
            {'style': 'google', 'checkClassAttributes': True},
            [],
            id='class-attributes-google',
        ),
        # A docstring in another style only gets DOC003 (style mismatch), not
        # DOC105 for its wrong default
        pytest.param(
            'style_mismatch/numpy.py',
            {'style': 'numpy', 'checkStyleMismatch': True},
            [
                'DOC003: Function/method `f`: Docstring style mismatch. (Please'
                ' read more at https://jsh9.github.io/pydoclint/style_mismatch.html'
                ' ). You specified "numpy" style, but the docstring is likely not'
                ' written in this style.',
            ],
            id='style-mismatch-numpy',
        ),
        pytest.param(
            'style_mismatch/google.py',
            {'style': 'google', 'checkStyleMismatch': True},
            [
                'DOC003: Function/method `f`: Docstring style mismatch. (Please'
                ' read more at https://jsh9.github.io/pydoclint/style_mismatch.html'
                ' ). You specified "google" style, but the docstring is likely'
                ' not written in this style.',
            ],
            id='style-mismatch-google',
        ),
    ],
)
def testDefaultsAreNotComparedInTheseCases(
        fixtureFile: str,
        options: dict[str, Any],
        expectedViolations: list[str],
) -> None:
    """
    Test the cases where, with ``--check-arg-defaults``, the documented
    defaults are not compared with the code even though the type-hint options
    turn off the comparison of types. (In all of them, the signature has no
    types and ``--arg-type-hints-in-signature`` is False.)
    """
    fixtureDir = DATA_DIR / 'edge_cases/37_untyped_arg_defaults'
    violations = _checkFile(
        filename=fixtureDir / fixtureFile,
        checkArgDefaults=True,
        argTypeHintsInSignature=False,
        **options,
    )
    assert list(map(str, violations)) == expectedViolations


@pytest.mark.parametrize('style', ['google', 'numpy'])
@pytest.mark.parametrize(
    ('fixture', 'options', 'expectedViolations'),
    [
        pytest.param(
            'function_args',
            {'argTypeHintsInSignature': False},
            [
                'DOC104: Function `wrongOrder`: Arguments are the same in the'
                ' docstring and the function signature, but are in a different'
                ' order.',
                'DOC104: Function `wrongOrderAndDefault`: Arguments are the same'
                ' in the docstring and the function signature, but are in a'
                ' different order.',
            ],
            id='function-args',
        ),
        pytest.param(
            'function_args',
            {'argTypeHintsInSignature': False, 'checkArgDefaults': True},
            [
                'DOC104: Function `wrongOrder`: Arguments are the same in the'
                ' docstring and the function signature, but are in a different'
                ' order.',
                'DOC104: Function `wrongOrderAndDefault`: Arguments are the same'
                ' in the docstring and the function signature, but are in a'
                ' different order.',
                # The defaults are still compared, as when the order is right
                'DOC105: Function `wrongOrderAndDefault`: Argument names match,'
                ' but type hints in these args do not match: b . (Note:'
                ' docstring arg defaults should look like: `, default=XXX`)',
            ],
            id='function-args-check-defaults',
        ),
        pytest.param(
            'class_attributes',
            {'argTypeHintsInSignature': False, 'checkClassAttributes': True},
            [
                'DOC604: Class `A`: Attributes are the same in docstring and'
                ' class def, but are in a different order.  (Please read'
                ' https://jsh9.github.io/pydoclint/checking_class_attributes.html'
                ' on how to correctly document class attributes.)',
            ],
            id='class-attributes',
        ),
    ],
)
def testReorderedArgsWithTypeHintCheckOff(
        style: str,
        fixture: str,
        options: dict[str, Any],
        expectedViolations: list[str],
) -> None:
    """
    Test args (or class attributes) documented in a different order, with
    ``--arg-type-hints-in-signature`` turned off.

    They get DOC104 (DOC604) for the order, but no DOC105 (DOC605) for their
    type hints, which aren't compared, just as when the order is right. See
    https://github.com/jsh9/pydoclint/issues/325.
    """
    fixtureDir = DATA_DIR / 'edge_cases/38_reordered_args' / fixture
    violations = _checkFile(
        filename=fixtureDir / f'{style}.py',
        style=style,
        **options,
    )
    assert list(map(str, violations)) == expectedViolations


@pytest.mark.parametrize(
    ('fixtureFile', 'style', 'expectedViolations'),
    [
        pytest.param(
            'numpy.py',
            'google',
            [
                'DOC003: Function/method `wrongOrder`: Docstring style mismatch.'
                ' (Please read more at'
                ' https://jsh9.github.io/pydoclint/style_mismatch.html ). You'
                ' specified "google" style, but the docstring is likely not'
                ' written in this style.',
                'DOC104: Function `wrongOrder`: Arguments are the same in the'
                ' docstring and the function signature, but are in a different'
                ' order.',
                'DOC003: Function/method `wrongOrderAndDefault`: Docstring style'
                ' mismatch. (Please read more at'
                ' https://jsh9.github.io/pydoclint/style_mismatch.html ). You'
                ' specified "google" style, but the docstring is likely not'
                ' written in this style.',
                'DOC104: Function `wrongOrderAndDefault`: Arguments are the same'
                ' in the docstring and the function signature, but are in a'
                ' different order.',
            ],
            id='numpy-docstrings-checked-as-google',
        ),
        pytest.param(
            'google.py',
            'numpy',
            [
                'DOC003: Function/method `wrongOrder`: Docstring style mismatch.'
                ' (Please read more at'
                ' https://jsh9.github.io/pydoclint/style_mismatch.html ). You'
                ' specified "numpy" style, but the docstring is likely not'
                ' written in this style.',
                'DOC104: Function `wrongOrder`: Arguments are the same in the'
                ' docstring and the function signature, but are in a different'
                ' order.',
                'DOC003: Function/method `wrongOrderAndDefault`: Docstring style'
                ' mismatch. (Please read more at'
                ' https://jsh9.github.io/pydoclint/style_mismatch.html ). You'
                ' specified "numpy" style, but the docstring is likely not'
                ' written in this style.',
                'DOC104: Function `wrongOrderAndDefault`: Arguments are the same'
                ' in the docstring and the function signature, but are in a'
                ' different order.',
            ],
            id='google-docstrings-checked-as-numpy',
        ),
    ],
)
def testReorderedArgsInAnotherStyle(
        fixtureFile: str,
        style: str,
        expectedViolations: list[str],
) -> None:
    """
    Test args documented in a different order, in a docstring written in
    another style (DOC003). Type hints aren't compared for such a docstring,
    even with both type-hint options on, so there's DOC104 for the order but no
    DOC105, just as when the order is right. See
    https://github.com/jsh9/pydoclint/issues/325.
    """
    fixtureDir = DATA_DIR / 'edge_cases/38_reordered_args/function_args'
    violations = _checkFile(
        filename=fixtureDir / fixtureFile,
        style=style,
        checkStyleMismatch=True,
    )
    assert list(map(str, violations)) == expectedViolations


@pytest.mark.parametrize('style', ['google', 'numpy'])
def testReorderedArgsWithEqualTypeHints(style: str) -> None:
    """
    Test args documented in a different order, whose type hints are equal but
    written differently (``Dict[str, int]`` and ``Dict[str,int]``). They only
    get DOC104 for the order. (They used to also get a DOC105 that listed no
    args. See https://github.com/jsh9/pydoclint/issues/339.)
    """
    fixtureDir = DATA_DIR / 'edge_cases/39_reordered_args_equal_type_hints'
    violations = _checkFile(filename=fixtureDir / f'{style}.py', style=style)
    assert list(map(str, violations)) == [
        'DOC104: Function `f`: Arguments are the same in the docstring and the'
        ' function signature, but are in a different order.',
    ]

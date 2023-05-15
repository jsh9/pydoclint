import ast
from typing import Optional, Tuple

from numpydoc.docscrape import NumpyDocString

from pydoclint.method_type import MethodType
from pydoclint.utils.astTypes import AllFunctionDef, ClassOrFunctionDef


def getFunctionId(node: AllFunctionDef) -> Tuple[int, int, str]:
    """
    Get unique identifier of a function def. We also need line and
    column number because different function can have identical names.
    """
    return node.lineno, node.col_offset, node.name


def detectMethodType(node: ast.FunctionDef) -> MethodType:
    """
    Detect whether the function def is an instance method,
    a classmethod, or a staticmethod.
    """
    if len(node.decorator_list) == 0:
        return MethodType.INSTANCE_METHOD

    # Traverse in reversed order, because it's possible to
    # stack `@classmethod` on top of `@staticmethod`, and we
    # only want the decorator closest to the method name
    # to count.
    for decorator in node.decorator_list[::-1]:
        if isinstance(decorator, ast.Name):
            if decorator.id == 'classmethod':
                return MethodType.CLASS_METHOD

            if decorator.id == 'staticmethod':
                return MethodType.STATIC_METHOD

    return MethodType.INSTANCE_METHOD


def isShortDocstring(docstringStruct: NumpyDocString) -> bool:
    """Detect whether the input is a short docstring."""
    return (
        (
            bool(docstringStruct.get('Summary'))
            or bool(docstringStruct.get('Extended Summary'))
        )
        and not bool(docstringStruct.get('Parameters'))
        and not bool(docstringStruct.get('Returns'))
        and not bool(docstringStruct.get('Yields'))
        and not bool(docstringStruct.get('Receives'))
        and not bool(docstringStruct.get('Raises'))
        and not bool(docstringStruct.get('Warns'))
        and not bool(docstringStruct.get('Other Parameters'))
        and not bool(docstringStruct.get('Attributes'))
        and not bool(docstringStruct.get('Methods'))
        and not bool(docstringStruct.get('See Also'))
        and not bool(docstringStruct.get('Notes'))
        and not bool(docstringStruct.get('Warnings'))
        and not bool(docstringStruct.get('References'))
        and not bool(docstringStruct.get('Examples'))
        and not bool(docstringStruct.get('index'))
    )


def getDocstring(node: ClassOrFunctionDef) -> str:
    """Get docstring from a class definition or a function definition"""
    docstring_: Optional[str] = ast.get_docstring(node)
    return '' if docstring_ is None else docstring_

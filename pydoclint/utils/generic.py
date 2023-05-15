import ast
from typing import Optional, Tuple

from numpydoc.docscrape import NumpyDocString

from pydoclint.method_type import MethodType
from pydoclint.utils.astTypes import ClassOrFunctionDef, FuncOrAsyncFuncDef


def getFunctionId(node: FuncOrAsyncFuncDef) -> Tuple[int, int, str]:
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


def generateMsgPrefix(
        node: FuncOrAsyncFuncDef,
        parent: ast.AST,
        appendColon: bool,
) -> str:
    """
    Generate violation message prefix.

    Parameters
    ----------
    node : FuncOrAsyncFuncDef
        The current node.
    parent : ast.AST
        The parent of the current node.
    appendColon : bool
        Whether to append a colon (':') at the end of the message prefix

    Returns
    -------
    str
        The violation message prefix.
    """
    isMethod: bool = isinstance(parent, ast.ClassDef)
    parentName: str = getNodeName(parent)
    selfName: str = getNodeName(node)

    colon = ':' if appendColon else ''

    if isMethod:
        return f'Method `{parentName}.{selfName}`{colon}'

    return f'Function `{selfName}`{colon}'


def getNodeName(node: ast.AST) -> str:
    """Get the name of an AST node"""
    if node is None:
        return ''

    return node.name if 'name' in node.__dict__ else ''

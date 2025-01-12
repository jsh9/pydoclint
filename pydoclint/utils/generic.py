from __future__ import annotations

import ast
import copy
import re
from typing import TYPE_CHECKING, Match

from pydoclint.utils.astTypes import ClassOrFunctionDef, FuncOrAsyncFuncDef
from pydoclint.utils.method_type import MethodType
from pydoclint.utils.violation import Violation

if TYPE_CHECKING:
    from pydoclint.utils.arg import Arg, ArgList


def collectFuncArgs(node: FuncOrAsyncFuncDef) -> list[ast.arg]:
    """
    Collect all arguments from a function node, and return them in
    their original order in the function signature.
    """
    allArgs: list[ast.arg] = []
    allArgs.extend(node.args.args)
    allArgs.extend(node.args.posonlyargs)
    allArgs.extend(node.args.kwonlyargs)

    if node.args.vararg is not None:
        try:
            vararg = copy.deepcopy(node.args.vararg)
        except RecursionError:
            # In rare occasions, using deepcopy could trigger recursion errors
            # if the underlying Python code is too complex. And example for
            # it is https://github.com/jsh9/pydoclint/issues/65
            vararg = copy.copy(node.args.vararg)

        # This is a hacky way to ensure that users write '*args' instead
        # of 'args' in the docstring, as per the style guide of numpy:
        # https://numpydoc.readthedocs.io/en/latest/format.html
        vararg.arg = '*' + vararg.arg

        # Not 'extend', because there can be only one vararg
        allArgs.append(vararg)

    if node.args.kwarg is not None:
        try:
            kwarg = copy.deepcopy(node.args.kwarg)
        except RecursionError:
            # In rare occasions, using deepcopy could trigger recursion errors
            # if the underlying Python code is too complex. And example for
            # it is https://github.com/jsh9/pydoclint/issues/65
            kwarg = copy.copy(node.args.kwarg)

        # This is a hacky way to ensure that users write '**kwargs' instead
        # of 'kwargs' in the docstring, as per the style guide of numpy:
        # https://numpydoc.readthedocs.io/en/latest/format.html
        kwarg.arg = '**' + kwarg.arg

        # not 'extend' because there can be only one vararg
        allArgs.append(kwarg)

    return sorted(  # sort to reconstruct the original order of arguments
        allArgs,
        key=lambda x: (x.lineno, x.col_offset),
        reverse=False,
    )


def getFunctionId(node: FuncOrAsyncFuncDef) -> tuple[int, int, str]:
    """
    Get unique identifier of a function def. We also need line and
    column number because different function can have identical names.

    Note: this function is no longer used by the actual code, but it is
    still used in unit tests. That's why we did not remove it.
    """
    return node.lineno, node.col_offset, node.name


def detectMethodType(node: FuncOrAsyncFuncDef) -> MethodType:
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


def getDocstring(node: ClassOrFunctionDef) -> str:
    """Get docstring from a class definition or a function definition"""
    docstring_: str | None = ast.get_docstring(node)
    return '' if docstring_ is None else docstring_


def generateClassMsgPrefix(node: ast.ClassDef, appendColon: bool) -> str:
    """
    Generate violation message prefix for classes.

    Parameters
    ----------
    node : ast.ClassDef
        The current node.
    appendColon : bool
        Whether to append a colon (':') at the end of the message prefix

    Returns
    -------
    str
        The violation message prefix
    """
    selfName: str = getNodeName(node)
    colon = ':' if appendColon else ''
    return f'Class `{selfName}`{colon}'


def generateFuncMsgPrefix(
        node: FuncOrAsyncFuncDef,
        parent: ast.AST,
        appendColon: bool,
) -> str:
    """
    Generate violation message prefix for function def.

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

    return getattr(node, 'name', '')


def stringStartsWith(string: str | None, substrings: tuple[str, ...]) -> bool:
    """Check whether the string starts with any of the substrings"""
    if string is None:
        return False

    for substring in substrings:
        if string.startswith(substring):
            return True

    return False


def stripQuotes(string: str | None) -> str | None:
    """
    Strip quotes (both double and single quotes) from the given string.
    Also, strip backticks (`) or double backticks (``) from the beginning
    and the end of the given string.  (Some people use backticks around
    type hints so that they show up more nicely on the HTML documentation
    page.)
    """
    if string is None:
        return None

    if string.startswith('``') and string.endswith('``') and len(string) > 4:
        string = string[2:-2]
    elif string.startswith('`') and string.endswith('`') and len(string) > 3:
        string = string[1:-1]

    return re.sub(r'Literal\[[^\]]+\]|[^L]+', _replacer, string)


def _replacer(match: Match[str]) -> str:
    # If the matched string starts with 'Literal', return it unmodified
    if match.group(0).startswith('Literal'):
        return match.group(0)

    # Otherwise, remove all quotes
    return match.group(0).replace('"', '').replace("'", '')


def appendArgsToCheckToV105(
        *,
        original_v105: Violation,
        funcArgs: ArgList,
        docArgs: ArgList,
) -> Violation:
    """Append the arg names to check to the error message of v105 or v605"""
    argsToCheck: list[Arg] = funcArgs.findArgsWithDifferentTypeHints(docArgs)
    argNames: str = ', '.join(_.name for _ in argsToCheck)
    return original_v105.appendMoreMsg(moreMsg=argNames)


def specialEqual(str1: str, str2: str) -> bool:
    """
    Check string equality but treat any single quotes as the same as
    double quotes, and also ignore line breaks in either strings.
    """
    if str1 == str2:
        return True  # using shortcuts to speed up evaluation

    if '\n' in str1 or '\n' in str2:
        str1 = str1.replace(' ', '').replace('\n', '')
        str2 = str2.replace(' ', '').replace('\n', '')

    if len(str1) != len(str2):
        return False  # using shortcuts to speed up evaluation

    quotes = {'"', "'"}
    for char1, char2 in zip(str1, str2):
        if char1 == char2:
            continue

        if char1 in quotes and char2 in quotes:
            continue

        return False

    return True


def doList1ItemsStartWithList2Items(
        list1: list[str],
        list2: list[str],
) -> bool:
    """
    Check whether all the elements in list1 start with the corresponding
    element in list2.
    """
    if len(list1) != len(list2):
        return False

    if list1 == list2:  # short-circuit, maybe faster than explicit for loop
        return True

    for elem1, elem2 in zip(list1, list2):
        if not elem1.startswith(elem2):
            return False

    return True

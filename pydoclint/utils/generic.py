import ast
import copy
import re
from typing import List, Match, Optional, Tuple

from pydoclint.utils.astTypes import ClassOrFunctionDef, FuncOrAsyncFuncDef
from pydoclint.utils.method_type import MethodType
from pydoclint.utils.violation import Violation


def collectFuncArgs(node: FuncOrAsyncFuncDef) -> List[ast.arg]:
    """
    Collect all arguments from a function node, and return them in
    their original order in the function signature.
    """
    allArgs: List[ast.arg] = []
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


def getFunctionId(node: FuncOrAsyncFuncDef) -> Tuple[int, int, str]:
    """
    Get unique identifier of a function def. We also need line and
    column number because different function can have identical names.

    Note: this function is no longer used by the actual code, but it is
    still used in unit tests. That's why we did not remove it.
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


def stringStartsWith(string: str, substrings: Tuple[str, ...]) -> bool:
    """Check whether the string starts with any of the substrings"""
    for substring in substrings:
        if string.startswith(substring):
            return True

    return False


def stripQuotes(string: Optional[str]) -> Optional[str]:
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
        funcArgs: 'ArgList',  # noqa: F821
        docArgs: 'ArgList',  # noqa: F821
) -> Violation:
    """Append the arg names to check to the error message of v105"""
    argsToCheck: List['Arg'] = funcArgs.findArgsWithDifferentTypeHints(docArgs)  # noqa: F821
    argNames: str = ', '.join(_.name for _ in argsToCheck)
    return original_v105.appendMoreMsg(moreMsg=argNames)


def specialEqual(str1: str, str2: str) -> bool:
    """
    Check string equality but treat any single quotes as the same as
    double quotes.
    """
    if str1 == str2:
        return True  # using shortcuts to speed up evaluation

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

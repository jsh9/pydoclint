import ast

from pydoclint.utils.ast_types import FuncOrAsyncFuncDef


def checkIsAbstractMethod(node: FuncOrAsyncFuncDef) -> bool:
    """Check whether ``node`` is an abstract method"""
    return checkMethodContainsSpecifiedDecorator(node, 'abstractmethod')


def checkIsPropertyMethod(node: FuncOrAsyncFuncDef) -> bool:
    """Check whether ``node`` is a method with @property decorator"""
    return checkMethodContainsSpecifiedDecorator(node, 'property')


def checkMethodContainsSpecifiedDecorator(
        node: FuncOrAsyncFuncDef,
        decorator: str,
) -> bool:
    """Check whether a method is decorated by the specified decorator"""
    return (
        isinstance(node.decorator_list, list)
        and len(node.decorator_list) > 0
        # Only the outermost (0th element) decorator counts
        and ast.unparse(node.decorator_list[0]) == decorator
    )

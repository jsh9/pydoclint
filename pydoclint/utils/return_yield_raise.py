import ast
from typing import Tuple, Type, Union

from pydoclint.utils import walk
from pydoclint.utils.annotation import unparseAnnotation
from pydoclint.utils.astTypes import BlockType, FuncOrAsyncFuncDef
from pydoclint.utils.generic import getFunctionId

ReturnType = Type[ast.Return]
ExprType = Type[ast.Expr]
YieldAndYieldFromTypes = Tuple[Type[ast.Yield], Type[ast.YieldFrom]]
FuncOrAsyncFuncTypes = Tuple[Type[ast.FunctionDef], Type[ast.AsyncFunctionDef]]


def hasReturnAnnotation(node: FuncOrAsyncFuncDef) -> bool:
    """Check whether the function node has a return type annotation"""
    return node.returns is not None


def isReturnAnnotationNone(node: FuncOrAsyncFuncDef) -> bool:
    """Check whether the return type annotation if `None`"""
    return _isNone(node.returns)


def hasGeneratorAsReturnAnnotation(node: FuncOrAsyncFuncDef) -> bool:
    """Check whether the function node has a 'Generator' return annotation"""
    if node.returns is None:
        return False

    returnAnnotation: str = unparseAnnotation(node.returns)
    return returnAnnotation.startswith('Generator')


def hasYieldStatements(node: FuncOrAsyncFuncDef) -> bool:
    """Check whether the function node has any yield statements"""
    thisId = getFunctionId(node)
    for child, parent in walk.walk(node):
        if isinstance(child, ast.Expr) and isinstance(
            child.value, (ast.Yield, ast.YieldFrom)
        ):
            if isinstance(parent, (ast.AsyncFunctionDef, ast.FunctionDef)):
                # Only return True if the parent is `node` (in other words,
                # this yield statement doesn't come from a nested function)
                parentId = getFunctionId(parent)
                if thisId == parentId:
                    return True

            if isinstance(parent, BlockType):
                return True

    return False


def hasReturnStatements(node: FuncOrAsyncFuncDef) -> bool:
    """Check whether the function node has any return statements"""
    return _hasReturnOrRaiseStatements(node, expectedNodeType=ast.Return)


def hasRaiseStatements(node: FuncOrAsyncFuncDef) -> bool:
    """Check whether the function node has any raise statements"""
    return _hasReturnOrRaiseStatements(node, expectedNodeType=ast.Raise)


def _hasReturnOrRaiseStatements(
        node: FuncOrAsyncFuncDef,
        expectedNodeType: Union[Type[ast.Return], Type[ast.Raise]],
) -> bool:
    thisId = getFunctionId(node)
    for child, parent in walk.walk(node):
        if isinstance(child, expectedNodeType):
            if isinstance(parent, (ast.AsyncFunctionDef, ast.FunctionDef)):
                # Only return True if the parent is `node` (in other words,
                # this statement doesn't come from a child function of `node`)
                parentId = getFunctionId(parent)
                if thisId == parentId:
                    return True

            if isinstance(parent, BlockType):
                return True

    return False


def _isNone(node: ast.AST) -> bool:
    return isinstance(node, ast.Constant) and node.value is None

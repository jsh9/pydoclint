import ast
from typing import Tuple, Type

from pydoclint.utils import walk
from pydoclint.utils.annotation import parseAnnotation
from pydoclint.utils.astTypes import Block, FuncOrAsyncFuncDef
from pydoclint.utils.generic import getFunctionId

ReturnType = Type[ast.Return]
ExprType = Type[ast.Expr]
YieldAndYieldFromTypes = Tuple[Type[ast.Yield], Type[ast.YieldFrom]]
FuncOrAsyncFuncTypes = Tuple[Type[ast.FunctionDef], Type[ast.AsyncFunctionDef]]


def hasReturnAnnotation(node: FuncOrAsyncFuncDef) -> bool:
    """Check whether the function node has a return type annotation"""
    return node.returns is not None


def hasGeneratorAsReturnAnnotation(node: FuncOrAsyncFuncDef) -> bool:
    """Check whether the function node has a 'Generator' return annotation"""
    if node.returns is None:
        return False

    returnAnnotation: str = parseAnnotation(node.returns)
    return returnAnnotation.startswith('Generator')


def hasReturnStatements(node: FuncOrAsyncFuncDef) -> bool:
    """Check whether the function node has any return statements"""
    thisId = getFunctionId(node)
    for child, parent in walk.walk(node):
        if isinstance(child, ast.Return):
            if isinstance(parent, (ast.AsyncFunctionDef, ast.FunctionDef)):
                # Only return True if the parent is `node` (in other words, if
                # this return statement doesn't come from a nested function)
                parentId = getFunctionId(parent)
                if thisId == parentId:
                    return True

            if isinstance(parent, Block):
                return True

    return False


def hasYieldStatements(node: FuncOrAsyncFuncDef) -> bool:
    """Check whether the function node has any yield statements"""
    thisId = getFunctionId(node)
    for child, parent in walk.walk(node):
        if isinstance(child, ast.Expr) and isinstance(
            child.value, (ast.Yield, ast.YieldFrom)
        ):
            if isinstance(parent, (ast.AsyncFunctionDef, ast.FunctionDef)):
                # Only return True if the parent is `node` (in other words, if
                # this return statement doesn't come from a nested function)
                parentId = getFunctionId(parent)
                if thisId == parentId:
                    return True

            if isinstance(parent, Block):
                return True

    return False

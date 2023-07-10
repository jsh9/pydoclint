import ast
from typing import Dict, Tuple, Type, Union

from pydoclint.utils import walk
from pydoclint.utils.annotation import unparseAnnotation
from pydoclint.utils.astTypes import BlockType, FuncOrAsyncFuncDef
from pydoclint.utils.generic import getFunctionId, stringStartsWith

ReturnType = Type[ast.Return]
ExprType = Type[ast.Expr]
YieldAndYieldFromTypes = Tuple[Type[ast.Yield], Type[ast.YieldFrom]]
FuncOrAsyncFuncTypes = Tuple[Type[ast.FunctionDef], Type[ast.AsyncFunctionDef]]
FuncOrAsyncFunc = (ast.FunctionDef, ast.AsyncFunctionDef)


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
    return stringStartsWith(returnAnnotation, ('Generator', 'AsyncGenerator'))


def hasIteratorOrIterableAsReturnAnnotation(node: FuncOrAsyncFuncDef) -> bool:
    """Check whether `node` has a 'Iterator' or 'Iterable' return annotation"""
    if node.returns is None:
        return False

    returnAnnotation: str = unparseAnnotation(node.returns)
    return stringStartsWith(
        returnAnnotation,
        ('Iterator', 'Iterable', 'AsyncIterator', 'AsyncIterable'),
    )


def hasYieldStatements(node: FuncOrAsyncFuncDef) -> bool:
    """Check whether the function node has any yield statements"""
    childLine: int = -999
    flag: bool = False

    # key: child lineno, value: (parent lineno, is parent a function?)
    familyLine: Dict[int, Tuple[int, bool]] = {}

    for child, parent in walk.walk(node):
        childLine = _getLineNum(child)
        parentLine = _getLineNum(parent)
        if childLine != -1 and parentLine != -1 and childLine != parentLine:
            isFunction = isinstance(parent, FuncOrAsyncFunc)
            familyLine[childLine] = (parentLine, isFunction)

        if isinstance(child, ast.Expr) and isinstance(
            child.value, (ast.Yield, ast.YieldFrom)
        ):
            if isinstance(parent, (ast.AsyncFunctionDef, ast.FunctionDef)):
                flag = True
                break

            if isinstance(parent, BlockType):
                flag = True
                break

    if flag:  # this means we found a `yield` statement within `node`
        parentFuncLineNum = _lookupParentFunc(familyLine, childLine)

        # We consider this `yield` a valid one only when its parent function
        # is indeed `node`
        if parentFuncLineNum == node.lineno:
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


def _getLineNum(node: ast.AST) -> int:
    try:
        lineNum = node.lineno
    except Exception:
        lineNum = -1

    return lineNum


def _lookupParentFunc(
        familyLine: Dict[int, Tuple[int, bool]],
        lineNum: int,
) -> int:
    if lineNum not in familyLine:
        return -999

    parentLineNum, isParentAFunction = familyLine[lineNum]

    if isParentAFunction:
        return parentLineNum

    return _lookupParentFunc(familyLine, parentLineNum)

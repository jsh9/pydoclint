import ast
from typing import Dict, Tuple, Type, Union

from pydoclint.utils import walk
from pydoclint.utils.annotation import unparseAnnotation
from pydoclint.utils.astTypes import BlockType, FuncOrAsyncFuncDef
from pydoclint.utils.generic import stringStartsWith

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
    childLineNum: int = -999
    foundYieldStmtTemp: bool = False  # "temp" b/c it may be false positive

    # key: child lineno, value: (parent lineno, is parent a function?)
    familyTree: Dict[int, Tuple[int, bool]] = {}

    for child, parent in walk.walk(node):
        childLineNum = _updateFamilyTree(child, parent, familyTree)

        if isinstance(child, ast.Expr) and isinstance(
            child.value, (ast.Yield, ast.YieldFrom)
        ):
            if isinstance(parent, (ast.AsyncFunctionDef, ast.FunctionDef)):
                foundYieldStmtTemp = True
                break

            if isinstance(parent, BlockType):
                foundYieldStmtTemp = True
                break

    return _foundExpectedStatement(
        foundStatementTemp=foundYieldStmtTemp,
        familyTree=familyTree,
        lineNumOfStatement=childLineNum,
        lineNumOfThisNode=node.lineno,
    )


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
    childLineNum: int = -999
    foundReturnOrRaiseStmt: bool = False

    # key: child lineno, value: (parent lineno, is parent a function?)
    familyTree: Dict[int, Tuple[int, bool]] = {}

    for child, parent in walk.walk(node):
        childLineNum = _updateFamilyTree(child, parent, familyTree)

        if isinstance(child, expectedNodeType):
            if isinstance(parent, (ast.AsyncFunctionDef, ast.FunctionDef)):
                foundReturnOrRaiseStmt = True
                break

            if isinstance(parent, BlockType):
                foundReturnOrRaiseStmt = True
                break

    return _foundExpectedStatement(
        foundStatementTemp=foundReturnOrRaiseStmt,
        familyTree=familyTree,
        lineNumOfStatement=childLineNum,
        lineNumOfThisNode=node.lineno,
    )


def _isNone(node: ast.AST) -> bool:
    return isinstance(node, ast.Constant) and node.value is None


def _updateFamilyTree(
        child: ast.AST,
        parent: ast.AST,
        familyTree: Dict[int, Tuple[int, bool]],
) -> int:
    childLine = _getLineNum(child)
    parentLine = _getLineNum(parent)
    if childLine != -1 and parentLine != -1 and childLine != parentLine:
        isFunction = isinstance(parent, FuncOrAsyncFunc)
        familyTree[childLine] = (parentLine, isFunction)

    return childLine


def _getLineNum(node: ast.AST) -> int:
    try:
        lineNum = node.lineno
    except Exception:
        lineNum = -1

    return lineNum


def _foundExpectedStatement(
        foundStatementTemp: bool,
        familyTree: Dict[int, Tuple[int, bool]],
        lineNumOfStatement: int,
        lineNumOfThisNode: int,
) -> bool:
    """
    Check whether we REALLY found the expected statment (return, yield,
    or raise).

    We do this by checking whether the line number of the parent function
    of the statement is the same as the line number of the node.

    If so, we know that this statement is an immediate child of the node.
    If not, we know that this statement is a child of a nested function of
    the node.
    """
    if not foundStatementTemp:
        return False

    parentFuncLineNum = _lookupParentFunc(familyTree, lineNumOfStatement)
    return parentFuncLineNum == lineNumOfThisNode


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

import ast
from typing import Callable, Dict, Generator, List, Optional, Tuple, Type

from pydoclint.utils import walk
from pydoclint.utils.astTypes import BlockType, FuncOrAsyncFuncDef
from pydoclint.utils.generic import getFullAttributeName, stringStartsWith
from pydoclint.utils.unparser_custom import unparseName

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


def _isNone(node: ast.AST) -> bool:
    return isinstance(node, ast.Constant) and node.value is None


def isReturnAnnotationNoReturn(node: FuncOrAsyncFuncDef) -> bool:
    """Check whether the return type annotation if `NoReturn`"""
    if node.returns is None:
        return False

    returnAnnotation: str = unparseName(node.returns)
    return returnAnnotation == 'NoReturn'


def hasGeneratorAsReturnAnnotation(node: FuncOrAsyncFuncDef) -> bool:
    """Check whether the function node has a 'Generator' return annotation"""
    if node.returns is None:
        return False

    returnAnno: str = unparseName(node.returns)
    return returnAnno in {'Generator', 'AsyncGenerator'} or stringStartsWith(
        returnAnno, ('Generator[', 'AsyncGenerator[')
    )


def hasIteratorOrIterableAsReturnAnnotation(node: FuncOrAsyncFuncDef) -> bool:
    """Check whether `node` has a 'Iterator' or 'Iterable' return annotation"""
    if node.returns is None:
        return False

    returnAnnotation: str = unparseName(node.returns)
    return returnAnnotation in {
        'Iterator',
        'Iterable',
        'AsyncIterator',
        'AsyncIterable',
    } or stringStartsWith(
        returnAnnotation,
        ('Iterator', 'Iterable', 'AsyncIterator', 'AsyncIterable'),
    )


def hasYieldStatements(node: FuncOrAsyncFuncDef) -> bool:
    """Check whether the function node has any yield statements"""

    def isThisNodeAYieldStmt(node_: ast.AST) -> bool:
        return isinstance(node_, ast.Expr) and isinstance(
            node_.value, (ast.Yield, ast.YieldFrom)
        )

    return _hasExpectedStatements(node, isThisNodeAYieldStmt)


def hasReturnStatements(node: FuncOrAsyncFuncDef) -> bool:
    """Check whether the function node has any return statements"""

    def isThisNodeAReturnStmt(node_: ast.AST) -> bool:
        return isinstance(node_, ast.Return)

    return _hasExpectedStatements(node, isThisNodeAReturnStmt)


def hasRaiseStatements(node: FuncOrAsyncFuncDef) -> bool:
    """Check whether the function node has any raise statements"""

    def isThisNodeARaiseStmt(node_: ast.AST) -> bool:
        return isinstance(node_, ast.Raise)

    return _hasExpectedStatements(node, isThisNodeARaiseStmt)


def getRaisedExceptions(node: FuncOrAsyncFuncDef) -> List[str]:
    """Get the raised exceptions in a function node as a sorted list"""
    return sorted(set(_getRaisedExceptions(node)))


def _getRaisedExceptions(
        node: FuncOrAsyncFuncDef,
) -> Generator[str, None, None]:
    """Yield the raised exceptions in a function node"""
    childLineNum: int = -999

    # key: child lineno, value: (parent lineno, is parent a function?)
    familyTree: Dict[int, Tuple[int, bool]] = {}

    currentParentExceptHandler: Optional[ast.ExceptHandler] = None

    # Depth-first guarantees the last-seen exception handler
    # is a parent of child.
    for child, parent in walk.walk_dfs(node):
        childLineNum = _updateFamilyTree(child, parent, familyTree)

        if isinstance(parent, ast.ExceptHandler):
            currentParentExceptHandler = parent

        if (
            isinstance(child, ast.Raise)
            and isinstance(
                parent,
                (ast.AsyncFunctionDef, ast.FunctionDef, BlockType),
            )
            and _confirmThisStmtIsNotWithinNestedFunc(
                foundStatementTemp=True,
                familyTree=familyTree,
                lineNumOfStatement=childLineNum,
                lineNumOfThisNode=node.lineno,
            )
        ):
            for subnode, _ in walk.walk_dfs(child):
                if isinstance(subnode, ast.Name):
                    if isinstance(child.exc, ast.Attribute):
                        # case: looks like m.n.exception
                        yield getFullAttributeName(child.exc)
                    elif isinstance(child.exc, ast.Call) and isinstance(
                        child.exc.func, ast.Attribute
                    ):
                        # case: looks like m.n.exception()
                        yield getFullAttributeName(child.exc.func)
                    elif (
                        currentParentExceptHandler
                        and currentParentExceptHandler.name
                        and subnode.id == currentParentExceptHandler.name
                    ):
                        # case: "except <> as e; raise e" -> we must yield the
                        # stuff in <>
                        #
                        # Note: if subnode.id != currentParentExceptHandler.name,
                        # the user is raising something not bound by
                        # this exception handler (meaning we should fall
                        # through to yielding the subnode.id)
                        yield from _extractExceptionsFromExcept(
                            currentParentExceptHandler
                        )
                    else:
                        yield subnode.id

                    break
            else:
                # if "raise" statement was alone, it must be inside an "except"
                if currentParentExceptHandler:
                    yield from _extractExceptionsFromExcept(
                        currentParentExceptHandler,
                    )


def _extractExceptionsFromExcept(
        node: ast.ExceptHandler,
) -> Generator[str, None, None]:
    if isinstance(node.type, ast.Name):
        yield node.type.id

    if isinstance(node.type, ast.Attribute):
        # case: looks like m.n.exception
        yield getFullAttributeName(node.type)

    if isinstance(node.type, ast.Tuple):
        for elt in node.type.elts:
            if isinstance(elt, ast.Attribute):
                # case: looks like m.n.exception
                yield getFullAttributeName(elt)
            elif isinstance(elt, ast.Name):
                yield elt.id


def _hasExpectedStatements(
        node: FuncOrAsyncFuncDef,
        isThisNodeAnExpectedStmt: Callable[[ast.AST], bool],
) -> bool:
    """
    Check whether the node contains an expected statement (return, yield, or
    raise).
    """
    childLineNum: int = -999
    foundExpectedStmt: bool = False

    # key: child lineno, value: (parent lineno, is parent a function?)
    familyTree: Dict[int, Tuple[int, bool]] = {}

    for child, parent in walk.walk(node):
        childLineNum = _updateFamilyTree(child, parent, familyTree)

        if isThisNodeAnExpectedStmt(child):
            if isinstance(parent, (ast.AsyncFunctionDef, ast.FunctionDef)):
                foundExpectedStmt = True
                break

            if isinstance(parent, BlockType):
                foundExpectedStmt = True
                break

    return _confirmThisStmtIsNotWithinNestedFunc(
        foundStatementTemp=foundExpectedStmt,
        familyTree=familyTree,
        lineNumOfStatement=childLineNum,
        lineNumOfThisNode=node.lineno,
    )


def _updateFamilyTree(
        child: ast.AST,
        parent: ast.AST,
        familyTree: Dict[int, Tuple[int, bool]],
) -> int:
    """
    Structure of `familyTree`:
        Key: line number of child node
        Value: (line number of parent node, whether this parent is a function)
    """
    childLine = _getLineNum(child)
    parentLine = _getLineNum(parent)
    if childLine != -1 and parentLine != -1 and childLine != parentLine:
        isFunction = isinstance(parent, FuncOrAsyncFunc)
        familyTree[childLine] = (parentLine, isFunction)

    return childLine


def _getLineNum(node: ast.AST) -> int:
    try:
        if 'lineno' in node.__dict__:  # normal case
            lineNum = node.lineno
        elif 'pattern' in node.__dict__:  # the node is a `case ...:`
            lineNum = node.pattern.lineno
        else:
            lineNum = node.lineno  # this could fail
    except Exception:
        lineNum = -1

    return lineNum


def _confirmThisStmtIsNotWithinNestedFunc(
        foundStatementTemp: bool,
        familyTree: Dict[int, Tuple[int, bool]],
        lineNumOfStatement: int,
        lineNumOfThisNode: int,
) -> bool:
    """
    Check whether we REALLY found the expected statement (return, yield,
    or raise).

    Returns True if this statement is not within a nested function of `node`.
    Returns False if otherwise.

    We do this by checking whether the line number of the parent function
    of the statement is the same as the line number of the node.
    """
    if not foundStatementTemp:
        return False

    parentFuncLineNum = _lookupParentFunc(familyTree, lineNumOfStatement)
    return parentFuncLineNum == lineNumOfThisNode


def _lookupParentFunc(
        familyLine: Dict[int, Tuple[int, bool]],
        lineNumOfChildNode: int,
) -> int:
    """
    Look up the parent function of the given child node.

    Recursion is used in this function, because the key-val pairs in
    `familyLine` only records immediate child-parent mapping.
    """
    if lineNumOfChildNode not in familyLine:
        return -999

    parentLineNum, isParentAFunction = familyLine[lineNumOfChildNode]

    if isParentAFunction:
        return parentLineNum

    return _lookupParentFunc(familyLine, parentLineNum)

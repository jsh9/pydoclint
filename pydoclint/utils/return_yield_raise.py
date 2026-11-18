from __future__ import annotations

import ast
import sys
from enum import Enum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Generator

from pydoclint.utils import walk
from pydoclint.utils.ast_types import BlockType, FuncOrAsyncFuncDef
from pydoclint.utils.unparser_custom import unparseName

ReturnType = type[ast.Return]
ExprType = type[ast.expr]
YieldAndYieldFromTypes = tuple[type[ast.Yield], type[ast.YieldFrom]]
FuncOrAsyncFuncTypes = tuple[type[ast.FunctionDef], type[ast.AsyncFunctionDef]]
FuncOrAsyncFunc = (ast.FunctionDef, ast.AsyncFunctionDef)
ExceptionEnv = dict[str, set[str]]

if sys.version_info >= (3, 11):
    TryStmtTypes = (ast.Try, ast.TryStar)
    TryStmt = ast.Try | ast.TryStar
else:  # Python 3.10 only, because this project doesn't support Python 3.9
    TryStmtTypes = (ast.Try,)
    TryStmt = ast.Try

_IGNORED_ANNOTATION_NAMES: frozenset[str] = frozenset({
    'Any',
    'Final',
    'Never',
    'NoReturn',
    'None',
    'Self',
    'object',
})
_UNWRAPPED_SUBSCRIPT_WRAPPERS: frozenset[str] = frozenset({
    'ClassVar',
    'Final',
    'Optional',
    'Type',
    'type',
})


class GeneratorAnnotationKind(Enum):
    """Supported generator-like return annotation kinds."""

    GENERATOR = auto()
    ASYNC_GENERATOR = auto()


def hasReturnAnnotation(node: FuncOrAsyncFuncDef) -> bool:
    """Check whether the function node has a return type annotation"""
    return node.returns is not None


def isReturnAnnotationNone(node: FuncOrAsyncFuncDef) -> bool:
    """Check whether the return type annotation if ``None``"""
    return _isNone(node.returns)


def _isNone(node: ast.expr | None) -> bool:
    return isinstance(node, ast.Constant) and node.value is None


def isReturnAnnotationNoReturn(node: FuncOrAsyncFuncDef) -> bool:
    """Check whether the return type annotation if ``NoReturn``"""
    if node.returns is None:
        return False

    returnAnnotation: str | None = unparseName(node.returns)
    return returnAnnotation == 'NoReturn'


def hasGeneratorAsReturnAnnotation(node: FuncOrAsyncFuncDef) -> bool:
    """Check whether the function node has a 'Generator' return annotation"""
    return getGeneratorAnnotationKind(node) is not None


def getGeneratorAnnotationKind(
        node: FuncOrAsyncFuncDef,
) -> GeneratorAnnotationKind | None:
    """Return the generator-like annotation kind for ``node`` if present."""
    returnAnno = _getReturnAnnotationName(node)
    if returnAnno == 'AsyncGenerator':
        return GeneratorAnnotationKind.ASYNC_GENERATOR

    if returnAnno == 'Generator':
        return GeneratorAnnotationKind.GENERATOR

    return None


def hasIteratorOrIterableAsReturnAnnotation(node: FuncOrAsyncFuncDef) -> bool:
    """
    Check whether ``node`` has a 'Iterator' or 'Iterable' return annotation
    """
    return _getReturnAnnotationName(node) in {
        'Iterator',
        'Iterable',
        'AsyncIterator',
        'AsyncIterable',
    }


def _getReturnAnnotationName(node: FuncOrAsyncFuncDef) -> str | None:
    """
    Get the terminal name of a bare or subscripted return annotation.

    Qualified names are recognized syntactically without resolving imports.
    Other expressions, including string forward references, are not unwrapped.
    """
    annotation = node.returns
    if isinstance(annotation, ast.Subscript):
        annotation = annotation.value

    if isinstance(annotation, ast.Name):
        return annotation.id

    if isinstance(annotation, ast.Attribute):
        name = annotation.attr
        while isinstance(annotation, ast.Attribute):
            annotation = annotation.value

        if isinstance(annotation, ast.Name):
            return name

    return None


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


def hasBareReturnStatements(node: FuncOrAsyncFuncDef) -> bool:
    """
    Check whether the function node has bare return statements (i.e., just a
    "return" without anything behind it)
    """

    def isThisNodeABareReturnStmt(node_: ast.AST) -> bool:
        return isinstance(node_, ast.Return) and node_.value is None

    return _hasExpectedStatements(node, isThisNodeABareReturnStmt)


def hasRaiseStatements(node: FuncOrAsyncFuncDef) -> bool:
    """Check whether the function node has any raise statements"""

    def isThisNodeARaiseStmt(node_: ast.AST) -> bool:
        return isinstance(node_, ast.Raise)

    return _hasExpectedStatements(node, isThisNodeARaiseStmt)


def hasAssertStatements(node: FuncOrAsyncFuncDef) -> bool:
    """Check whether the function node has any assert statements"""

    def isThisNodeAnAssertStmt(node_: ast.AST) -> bool:
        return isinstance(node_, ast.Assert)

    return _hasExpectedStatements(node, isThisNodeAnAssertStmt)


def getRaisedExceptions(
        node: FuncOrAsyncFuncDef,
        shouldDeclareAssertError: bool = False,  # noqa: FBT001, FBT002
) -> list[str]:
    """Get the raised exceptions in a function node as a sorted list"""
    return sorted(set(_getRaisedExceptions(node, shouldDeclareAssertError)))


class _RaiseScanState:
    __slots__ = (
        'activeExceptHandlers',
        'env',
        'loopExitEnvs',
        'raisedExceptions',
        'shouldDeclareAssertError',
    )

    def __init__(
            self,
            *,
            env: ExceptionEnv,
            shouldDeclareAssertError: bool,
            raisedExceptions: list[str],
            activeExceptHandlers: list[ast.ExceptHandler],
            loopExitEnvs: list[ExceptionEnv] | None = None,
    ) -> None:
        self.env = env
        self.shouldDeclareAssertError = shouldDeclareAssertError
        self.raisedExceptions = raisedExceptions
        self.activeExceptHandlers = activeExceptHandlers
        self.loopExitEnvs = loopExitEnvs

    def withEnv(
            self,
            env: ExceptionEnv,
            *,
            loopExitEnvs: list[ExceptionEnv] | None,
    ) -> _RaiseScanState:
        return _RaiseScanState(
            env=env,
            shouldDeclareAssertError=self.shouldDeclareAssertError,
            raisedExceptions=self.raisedExceptions,
            activeExceptHandlers=self.activeExceptHandlers,
            loopExitEnvs=loopExitEnvs,
        )


def _getRaisedExceptions(
        node: FuncOrAsyncFuncDef,
        shouldDeclareAssertError: bool = False,  # noqa: FBT001, FBT002
) -> Generator[str, None, None]:
    """Yield the raised exceptions or asserts in a function node"""
    state = _RaiseScanState(
        env=_collectFuncArgExceptionEnv(node),
        shouldDeclareAssertError=shouldDeclareAssertError,
        raisedExceptions=[],
        activeExceptHandlers=[],
    )
    _visitStatementsForRaises(node.body, state)
    yield from state.raisedExceptions


def _copyExceptionEnv(env: ExceptionEnv) -> ExceptionEnv:
    return {name: set(excNames) for name, excNames in env.items() if excNames}


def _mergeExceptionEnvs(envs: list[ExceptionEnv]) -> ExceptionEnv:
    merged: ExceptionEnv = {}
    for env in envs:
        for name, excNames in env.items():
            if excNames:
                merged.setdefault(name, set()).update(excNames)

    return merged


def _replaceExceptionEnv(target: ExceptionEnv, source: ExceptionEnv) -> None:
    target.clear()
    target.update(source)


def _hasNameRoot(node: ast.expr) -> bool:
    current: ast.expr = node
    while isinstance(current, ast.Attribute):
        current = current.value

    return isinstance(current, ast.Name)


def _resolveAttributeNames(
        node: ast.Attribute,
        env: ExceptionEnv,
) -> set[str]:
    attrs: list[str] = []
    current: ast.expr = node
    while isinstance(current, ast.Attribute):
        attrs.append(current.attr)
        current = current.value

    if not isinstance(current, ast.Name):
        return set()

    suffix = '.' + '.'.join(reversed(attrs))
    if current.id in env:
        return {f'{base}{suffix}' for base in env[current.id]}

    return {f'{current.id}{suffix}'}


def _getTerminalAnnotationName(node: ast.expr) -> str | None:
    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute) and _hasNameRoot(node):
        return node.attr

    return None


def _extractExceptionNamesFromAnnotation(
        annotation: ast.expr | None,
) -> set[str]:
    if annotation is None:
        return set()

    if isinstance(annotation, ast.Constant):
        if isinstance(annotation.value, str):
            try:
                parsed = ast.parse(annotation.value, mode='eval').body
            except SyntaxError:
                return set()

            return _extractExceptionNamesFromAnnotation(parsed)

        return set()

    if isinstance(annotation, ast.Name):
        if annotation.id in _IGNORED_ANNOTATION_NAMES:
            return set()

        return {annotation.id}

    if isinstance(annotation, ast.Attribute):
        if annotation.attr in _IGNORED_ANNOTATION_NAMES or not _hasNameRoot(
            annotation
        ):
            return set()

        return {unparseName(annotation)}

    if isinstance(annotation, ast.BinOp) and isinstance(
        annotation.op, ast.BitOr
    ):
        return _extractExceptionNamesFromAnnotation(
            annotation.left
        ) | _extractExceptionNamesFromAnnotation(annotation.right)

    if isinstance(annotation, ast.Subscript):
        return _extractExceptionNamesFromSubscript(annotation)

    return set()


def _extractExceptionNamesFromSubscript(
        annotation: ast.Subscript,
) -> set[str]:
    wrapperName = _getTerminalAnnotationName(annotation.value)
    if wrapperName == 'Union':
        if isinstance(annotation.slice, ast.Tuple):
            names: set[str] = set()
            for elt in annotation.slice.elts:
                names.update(_extractExceptionNamesFromAnnotation(elt))

            return names

        return _extractExceptionNamesFromAnnotation(annotation.slice)

    if wrapperName in _UNWRAPPED_SUBSCRIPT_WRAPPERS and not isinstance(
        annotation.slice, ast.Tuple
    ):
        return _extractExceptionNamesFromAnnotation(annotation.slice)

    if (
        wrapperName == 'Annotated'
        and isinstance(annotation.slice, ast.Tuple)
        and len(annotation.slice.elts) > 0
    ):
        return _extractExceptionNamesFromAnnotation(annotation.slice.elts[0])

    if _hasNameRoot(annotation.value) and wrapperName not in (
        _IGNORED_ANNOTATION_NAMES
    ):
        return {unparseName(annotation)}

    return set()


def _collectFuncArgExceptionEnv(node: FuncOrAsyncFuncDef) -> ExceptionEnv:
    env: ExceptionEnv = {}
    allArgs = [
        *node.args.posonlyargs,
        *node.args.args,
        *node.args.kwonlyargs,
    ]
    for arg in allArgs:
        annoTypes = _extractExceptionNamesFromAnnotation(arg.annotation)
        if annoTypes:
            env[arg.arg] = annoTypes

    return env


def _unwrapRaiseExpr(expr: ast.expr) -> ast.expr:
    current: ast.expr = expr
    while True:
        if isinstance(current, ast.NamedExpr):
            current = current.value
            continue

        if (
            isinstance(current, ast.Call)
            and isinstance(current.func, ast.Attribute)
            and current.func.attr == 'with_traceback'
        ):
            current = current.func.value
            continue

        return current


def _extractExceptionNamesFromValue(
        expr: ast.expr,
        env: ExceptionEnv,
) -> set[str]:
    unwrapped = _unwrapRaiseExpr(expr)
    if isinstance(unwrapped, ast.Name):
        return set(env.get(unwrapped.id, set()))

    if isinstance(unwrapped, ast.Call):
        if isinstance(unwrapped.func, ast.Name):
            if unwrapped.func.id in env:
                return set(env[unwrapped.func.id])

            return {unwrapped.func.id}

        if isinstance(unwrapped.func, ast.Attribute):
            return _resolveAttributeNames(unwrapped.func, env)

        return set()

    if isinstance(unwrapped, ast.IfExp):
        return _extractExceptionNamesFromValue(
            unwrapped.body, env
        ) | _extractExceptionNamesFromValue(unwrapped.orelse, env)

    if isinstance(unwrapped, ast.BoolOp):
        names: set[str] = set()
        for val in unwrapped.values:
            names.update(_extractExceptionNamesFromValue(val, env))

        return names

    return set()


def _applyNamedExprs(node: ast.AST, env: ExceptionEnv) -> None:
    for child in ast.iter_child_nodes(node):
        if isinstance(
            child,
            (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda),
        ):
            continue

        _applyNamedExprs(child, env)

    if isinstance(node, ast.NamedExpr) and isinstance(node.target, ast.Name):
        resolved = _extractExceptionNamesFromValue(node.value, env)
        if resolved:
            env[node.target.id] = resolved
        else:
            env.pop(node.target.id, None)


def _clearTargetNames(target: ast.AST, env: ExceptionEnv) -> None:
    if isinstance(target, ast.Name):
        env.pop(target.id, None)
        return

    for child in ast.iter_child_nodes(target):
        _clearTargetNames(child, env)


def _assignTarget(
        target: ast.expr,
        value: ast.expr,
        sourceEnv: ExceptionEnv,
        targetEnv: ExceptionEnv,
) -> None:
    if isinstance(target, ast.Name):
        resolved = _extractExceptionNamesFromValue(value, sourceEnv)
        if resolved:
            targetEnv[target.id] = resolved
        else:
            targetEnv.pop(target.id, None)

        return

    if (
        isinstance(target, (ast.Tuple, ast.List))
        and isinstance(value, (ast.Tuple, ast.List))
        and len(target.elts) == len(value.elts)
        and not any(isinstance(elt, ast.Starred) for elt in target.elts)
    ):
        for subTarget, subValue in zip(target.elts, value.elts, strict=False):
            _assignTarget(subTarget, subValue, sourceEnv, targetEnv)

        return

    _clearTargetNames(target, targetEnv)


def _visitStatementsForRaises(
        stmts: list[ast.stmt],
        state: _RaiseScanState,
) -> bool:
    canFallThrough = True
    for stmt in stmts:
        stmtFallsThrough = _visitSingleStmtForRaises(stmt, state)
        if not stmtFallsThrough:
            canFallThrough = False

    return canFallThrough


def _visitSingleStmtForRaises(
        stmt: ast.stmt,
        state: _RaiseScanState,
) -> bool:
    if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        for fieldName, fieldVal in ast.iter_fields(stmt):
            if fieldName == 'body':
                continue

            items = fieldVal if isinstance(fieldVal, list) else [fieldVal]
            for item in items:
                if isinstance(item, ast.AST):
                    _applyNamedExprs(item, state.env)

        state.env.pop(stmt.name, None)
        return True

    if isinstance(stmt, ast.Raise):
        _applyNamedExprs(stmt, state.env)
        state.raisedExceptions.extend(
            _extractExceptionsFromRaiseStmt(
                stmt, state.env, state.activeExceptHandlers
            )
        )
        return False

    if isinstance(stmt, ast.Assert):
        _applyNamedExprs(stmt, state.env)
        if state.shouldDeclareAssertError:
            state.raisedExceptions.append(
                'AssertionError (implicitly from the `assert` statement)'
            )

        return True

    if isinstance(stmt, ast.Return):
        _applyNamedExprs(stmt, state.env)
        return False

    if isinstance(stmt, (ast.Break, ast.Continue)):
        if state.loopExitEnvs is not None:
            state.loopExitEnvs.append(_copyExceptionEnv(state.env))

        return False

    if isinstance(
        stmt, (ast.Assign, ast.AnnAssign, ast.AugAssign, ast.Delete)
    ):
        _updateEnvFromAssignmentOrDelete(stmt, state.env)
        return True

    return _visitCompoundStmtForRaises(stmt, state)


def _updateEnvFromAssignmentOrDelete(
        stmt: ast.Assign | ast.AnnAssign | ast.AugAssign | ast.Delete,
        env: ExceptionEnv,
) -> None:
    if isinstance(stmt, ast.Assign):
        _applyNamedExprs(stmt.value, env)
        snapshot = _copyExceptionEnv(env)
        for target in stmt.targets:
            _assignTarget(target, stmt.value, snapshot, env)

        return

    if isinstance(stmt, ast.AnnAssign):
        if stmt.value is not None:
            _applyNamedExprs(stmt.value, env)

        if isinstance(stmt.target, ast.Name):
            annoTypes = _extractExceptionNamesFromAnnotation(stmt.annotation)
            if annoTypes:
                env[stmt.target.id] = annoTypes
            elif stmt.value is not None:
                _assignTarget(stmt.target, stmt.value, env, env)
            else:
                env.pop(stmt.target.id, None)

        return

    if isinstance(stmt, ast.AugAssign):
        _applyNamedExprs(stmt.value, env)
        _clearTargetNames(stmt.target, env)
        return

    for target in stmt.targets:
        _clearTargetNames(target, env)


def _visitCompoundStmtForRaises(
        stmt: ast.stmt,
        state: _RaiseScanState,
) -> bool:
    if isinstance(stmt, ast.If):
        return _visitIfStmtForRaises(stmt, state)

    if isinstance(stmt, (ast.For, ast.AsyncFor, ast.While)):
        return _visitLoopStmtForRaises(stmt, state)

    if isinstance(stmt, (ast.With, ast.AsyncWith)):
        return _visitWithStmtForRaises(stmt, state)

    if isinstance(stmt, ast.Match):
        return _visitMatchStmtForRaises(stmt, state)

    if isinstance(stmt, TryStmtTypes):
        return _visitTryStmtForRaises(stmt, state)

    if isinstance(stmt, (ast.Import, ast.ImportFrom)):
        for alias in stmt.names:
            boundName = alias.asname or alias.name.split('.')[0]
            state.env.pop(boundName, None)

        return True

    _applyNamedExprs(stmt, state.env)
    return True


def _visitIfStmtForRaises(
        stmt: ast.If,
        state: _RaiseScanState,
) -> bool:
    _applyNamedExprs(stmt.test, state.env)
    bodyEnv = _copyExceptionEnv(state.env)
    elseEnv = _copyExceptionEnv(state.env)

    bodyFalls = _visitStatementsForRaises(
        stmt.body,
        state.withEnv(bodyEnv, loopExitEnvs=state.loopExitEnvs),
    )
    elseFalls = _visitStatementsForRaises(
        stmt.orelse,
        state.withEnv(elseEnv, loopExitEnvs=state.loopExitEnvs),
    )

    outEnvs: list[ExceptionEnv] = []
    if bodyFalls:
        outEnvs.append(bodyEnv)

    if elseFalls:
        outEnvs.append(elseEnv)

    if not outEnvs:
        return False

    _replaceExceptionEnv(state.env, _mergeExceptionEnvs(outEnvs))
    return True


def _visitLoopStmtForRaises(
        stmt: ast.For | ast.AsyncFor | ast.While,
        state: _RaiseScanState,
) -> bool:
    if isinstance(stmt, ast.While):
        _applyNamedExprs(stmt.test, state.env)
    else:
        _applyNamedExprs(stmt.iter, state.env)

    bodyEnv = _copyExceptionEnv(state.env)
    if isinstance(stmt, (ast.For, ast.AsyncFor)):
        _clearTargetNames(stmt.target, bodyEnv)

    loopExitEnvs: list[ExceptionEnv] = []
    bodyFalls = _visitStatementsForRaises(
        stmt.body,
        state.withEnv(bodyEnv, loopExitEnvs=loopExitEnvs),
    )

    elseEnv = _copyExceptionEnv(state.env)
    elseFalls = _visitStatementsForRaises(
        stmt.orelse,
        state.withEnv(elseEnv, loopExitEnvs=state.loopExitEnvs),
    )

    outEnvs: list[ExceptionEnv] = [
        _copyExceptionEnv(state.env),
        *loopExitEnvs,
    ]
    if bodyFalls:
        outEnvs.append(bodyEnv)

    if elseFalls:
        outEnvs.append(elseEnv)

    _replaceExceptionEnv(state.env, _mergeExceptionEnvs(outEnvs))
    return True


def _visitWithStmtForRaises(
        stmt: ast.With | ast.AsyncWith,
        state: _RaiseScanState,
) -> bool:
    for item in stmt.items:
        _applyNamedExprs(item.context_expr, state.env)
        if item.optional_vars is not None:
            _clearTargetNames(item.optional_vars, state.env)

    return _visitStatementsForRaises(stmt.body, state)


def _applyMatchPatternBindings(
        pattern: ast.pattern,
        env: ExceptionEnv,
) -> None:
    if isinstance(pattern, ast.MatchAs):
        if pattern.pattern is not None:
            _applyMatchPatternBindings(pattern.pattern, env)

        if pattern.name is not None:
            if isinstance(pattern.pattern, ast.MatchClass) and _hasNameRoot(
                pattern.pattern.cls
            ):
                env[pattern.name] = {unparseName(pattern.pattern.cls)}
            else:
                env.pop(pattern.name, None)

        return

    for child in ast.iter_child_nodes(pattern):
        if isinstance(child, ast.pattern):
            _applyMatchPatternBindings(child, env)


def _visitMatchStmtForRaises(
        stmt: ast.Match,
        state: _RaiseScanState,
) -> bool:
    _applyNamedExprs(stmt.subject, state.env)
    outEnvs: list[ExceptionEnv] = []
    hasIrrefutableCase = False

    for case in stmt.cases:
        caseEnv = _copyExceptionEnv(state.env)
        _applyMatchPatternBindings(case.pattern, caseEnv)
        if case.guard is not None:
            _applyNamedExprs(case.guard, caseEnv)
        elif (
            isinstance(case.pattern, ast.MatchAs)
            and case.pattern.pattern is None
        ):
            hasIrrefutableCase = True

        caseFalls = _visitStatementsForRaises(
            case.body,
            state.withEnv(caseEnv, loopExitEnvs=state.loopExitEnvs),
        )
        if caseFalls:
            outEnvs.append(caseEnv)

    if not hasIrrefutableCase:
        outEnvs.append(_copyExceptionEnv(state.env))

    if not outEnvs:
        return False

    _replaceExceptionEnv(state.env, _mergeExceptionEnvs(outEnvs))
    return True


def _visitTryStmtForRaises(
        stmt: TryStmt,
        state: _RaiseScanState,
) -> bool:
    preTryEnv = _copyExceptionEnv(state.env)
    tryEnv = _copyExceptionEnv(state.env)
    tryFalls = _visitStatementsForRaises(
        stmt.body,
        state.withEnv(tryEnv, loopExitEnvs=state.loopExitEnvs),
    )

    handlerBaseEnv = _mergeExceptionEnvs([preTryEnv, tryEnv])
    postTryEnvs: list[ExceptionEnv] = []

    for handler in stmt.handlers:
        handlerEnv = _copyExceptionEnv(handlerBaseEnv)
        caughtTypes = set(_extractExceptionsFromExcept(handler))
        if handler.name is not None:
            if caughtTypes:
                handlerEnv[handler.name] = caughtTypes
            else:
                handlerEnv.pop(handler.name, None)

        state.activeExceptHandlers.append(handler)
        try:
            handlerFalls = _visitStatementsForRaises(
                handler.body,
                state.withEnv(handlerEnv, loopExitEnvs=state.loopExitEnvs),
            )
        finally:
            state.activeExceptHandlers.pop()

        if handler.name is not None:
            handlerEnv.pop(handler.name, None)

        if handlerFalls:
            postTryEnvs.append(handlerEnv)

    if stmt.orelse:
        if tryFalls:
            elseEnv = _copyExceptionEnv(tryEnv)
            elseFalls = _visitStatementsForRaises(
                stmt.orelse,
                state.withEnv(elseEnv, loopExitEnvs=state.loopExitEnvs),
            )
            if elseFalls:
                postTryEnvs.append(elseEnv)
    elif tryFalls:
        postTryEnvs.append(tryEnv)

    if not stmt.finalbody:
        if not postTryEnvs:
            return False

        _replaceExceptionEnv(state.env, _mergeExceptionEnvs(postTryEnvs))
        return True

    finallyEnv = (
        _mergeExceptionEnvs(postTryEnvs)
        if postTryEnvs
        else _copyExceptionEnv(handlerBaseEnv)
    )
    finallyFalls = _visitStatementsForRaises(
        stmt.finalbody,
        state.withEnv(finallyEnv, loopExitEnvs=state.loopExitEnvs),
    )
    if not finallyFalls or not postTryEnvs:
        return False

    _replaceExceptionEnv(state.env, finallyEnv)
    return True


def _extractExceptionsFromCallExpr(
        callExpr: ast.Call,
        env: ExceptionEnv,
) -> list[str] | None:
    if isinstance(callExpr.func, ast.Name):
        if callExpr.func.id in env:
            return list(env[callExpr.func.id])

        return [callExpr.func.id]

    if isinstance(callExpr.func, ast.Attribute):
        resolvedAttrs = _resolveAttributeNames(callExpr.func, env)
        if resolvedAttrs:
            return sorted(resolvedAttrs)

        if any(
            isinstance(sub, ast.Name)
            for sub, _ in walk.walk_dfs(callExpr.func)
        ):
            return [unparseName(callExpr.func)]

    return None


def _extractExceptionsFromRaiseStmt(
        stmt: ast.Raise,
        env: ExceptionEnv,
        activeExceptHandlers: list[ast.ExceptHandler],
) -> Generator[str, None, None]:
    if stmt.exc is None:
        if activeExceptHandlers:
            yield from _extractExceptionsFromExcept(activeExceptHandlers[-1])

        return

    excExpr = _unwrapRaiseExpr(stmt.exc)
    if isinstance(excExpr, ast.Name):
        if excExpr.id in env:
            yield from env[excExpr.id]
        elif (
            activeExceptHandlers
            and activeExceptHandlers[-1].name == excExpr.id
        ):
            yield from _extractExceptionsFromExcept(activeExceptHandlers[-1])
        else:
            yield excExpr.id

        return

    if isinstance(excExpr, ast.Attribute):
        if any(isinstance(sub, ast.Name) for sub, _ in walk.walk_dfs(excExpr)):
            yield unparseName(excExpr)

        return

    if isinstance(excExpr, ast.Call):
        callNames = _extractExceptionsFromCallExpr(excExpr, env)
        if callNames is not None:
            yield from callNames
            return

    if isinstance(excExpr, (ast.IfExp, ast.BoolOp)):
        resolved = _extractExceptionNamesFromValue(excExpr, env)
        if resolved:
            yield from resolved
            return

    for subnode, _ in walk.walk_dfs(stmt):
        if isinstance(subnode, ast.Name):
            yield subnode.id
            return

    if activeExceptHandlers:
        yield from _extractExceptionsFromExcept(activeExceptHandlers[-1])


def _extractExceptionsFromExcept(
        node: ast.ExceptHandler,
) -> Generator[str, None, None]:
    if isinstance(node.type, ast.Name):
        yield node.type.id

    exceptionName: str | None

    if isinstance(node.type, ast.Attribute):
        # case: looks like m.n.exception
        exceptionName = unparseName(node.type)
        assert isinstance(exceptionName, str)
        yield exceptionName

    if isinstance(node.type, ast.Tuple):
        for elt in node.type.elts:
            if isinstance(elt, ast.Attribute):
                # case: looks like m.n.exception
                exceptionName = unparseName(elt)
                assert isinstance(exceptionName, str)
                yield exceptionName
            elif isinstance(elt, ast.Name):
                yield elt.id


def _hasExpectedStatements(
        node: FuncOrAsyncFuncDef,
        isThisNodeAnExpectedStmt: Callable[[ast.AST], bool],
) -> bool:
    """
    Check whether the node contains an expected statement (return, yield,
    raise, or assert).
    """
    childLineNum: int = -999
    foundExpectedStmt: bool = False

    # key: child lineno, value: (parent lineno, is parent a function?)
    familyTree: dict[int, tuple[int, bool]] = {}

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
        familyTree: dict[int, tuple[int, bool]],
) -> int:
    """
    Structure of ``familyTree``: Key: line number of child node; Value: (line
    number of parent node, whether this parent is a function)
    """
    childLine = _getLineNum(child)
    parentLine = _getLineNum(parent)
    if childLine != -1 and parentLine != -1 and childLine != parentLine:  # noqa: PLR1714
        isFunction = isinstance(parent, FuncOrAsyncFunc)
        familyTree[childLine] = (parentLine, isFunction)

    return childLine


def _getLineNum(node: ast.AST) -> int:
    lineNum = getattr(node, 'lineno', None)
    if isinstance(lineNum, int):
        return lineNum

    # A ``match`` case stores its source location on the pattern.
    pattern = getattr(node, 'pattern', None)
    patternLineNum = getattr(pattern, 'lineno', None)
    if isinstance(patternLineNum, int):
        return patternLineNum

    return -1


def _confirmThisStmtIsNotWithinNestedFunc(
        foundStatementTemp: bool,  # noqa: FBT001
        familyTree: dict[int, tuple[int, bool]],
        lineNumOfStatement: int,
        lineNumOfThisNode: int,
) -> bool:
    """
    Check whether we REALLY found the expected statement (return, yield, raise,
    or assert).

    Returns True if this statement is not within a nested function of ``node``.
    Returns False if otherwise.

    We do this by checking whether the line number of the parent function of
    the statement is the same as the line number of the node.
    """
    if not foundStatementTemp:
        return False

    parentFuncLineNum = _lookupParentFunc(familyTree, lineNumOfStatement)
    return parentFuncLineNum == lineNumOfThisNode


def _lookupParentFunc(
        familyLine: dict[int, tuple[int, bool]],
        lineNumOfChildNode: int,
) -> int:
    """
    Look up the parent function of the given child node.

    Recursion is used in this function, because the key-val pairs in
    ``familyLine`` only records immediate child-parent mapping.
    """
    if lineNumOfChildNode not in familyLine:
        return -999

    parentLineNum, isParentAFunction = familyLine[lineNumOfChildNode]

    if isParentAFunction:
        return parentLineNum

    return _lookupParentFunc(familyLine, parentLineNum)

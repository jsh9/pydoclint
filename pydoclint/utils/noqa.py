from __future__ import annotations

import ast
import re
import tokenize
from io import StringIO
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

    from pydoclint.utils.ast_types import ClassOrFunctionDef

ALLOWED_NOQA_LOCATIONS = {'definition', 'docstring'}
DOC_CODE_PATTERN = re.compile(r'DOC\d{3}', flags=re.IGNORECASE)


def parseNoqaComment(comment: str) -> set[str]:
    """
    Extract DOCxxx violation codes from a ``# noqa`` style comment.

    Parameters
    ----------
    comment : str
        The raw comment text, including the leading ``#``.

    Returns
    -------
    set[str]
        A set of uppercase DOC error codes found in the comment.
    """
    commentBody = comment.lstrip('#').strip()
    if not commentBody:
        return set()

    noqaMatch = re.search(r'\bnoqa\b', commentBody, flags=re.IGNORECASE)
    if noqaMatch is None:
        return set()

    remainder = commentBody[noqaMatch.end() :]
    remainder = remainder.lstrip()
    if not remainder.startswith(':'):
        return set()

    remainder = remainder[1:]
    return {
        match.group(0).upper()
        for match in DOC_CODE_PATTERN.finditer(remainder)
    }


def collectNoqaCodesByLine(src: str) -> dict[int, set[str]]:
    """
    Collect DOC codes from ``# noqa`` comments for each source line.

    Parameters
    ----------
    src : str
        The source code to tokenize.

    Returns
    -------
    dict[int, set[str]]
        Mapping from line numbers to the DOC codes declared on that line.
    """
    codesByLine: dict[int, set[str]] = {}
    reader = StringIO(src).readline

    for token in tokenize.generate_tokens(reader):
        if token.type != tokenize.COMMENT:
            continue

        codes = parseNoqaComment(token.string)
        if not codes:
            continue

        codesByLine.setdefault(token.start[0], set()).update(codes)

    return codesByLine


def collectNativeNoqaSuppression(
        *,
        tree: ast.AST,
        codesByLine: dict[int, set[str]],
        location: str,
) -> dict[int, set[str]]:
    """
    Determine which DOC codes are suppressed for each definition line.

    Parameters
    ----------
    tree : ast.AST
        Parsed syntax tree of the file.
    codesByLine : dict[int, set[str]]
        Mapping from line numbers to the DOC codes provided by comments.
    location : str
        Where the NOQA comments are expected. Either ``definition`` or
        ``docstring``.

    Returns
    -------
    dict[int, set[str]]
        Mapping from definition line numbers (``node.lineno``) to the set of
        DOC codes suppressed for that definition.

    Raises
    ------
    ValueError
        If ``location`` is not one of ``{"definition", "docstring"}``.
    """
    if location not in ALLOWED_NOQA_LOCATIONS:
        raise ValueError(
            'Invalid native NOQA location; must be "definition" or "docstring"'
        )

    definitionLineToCodes: dict[int, set[str]] = {}

    for node in _iterDocstringOwners(tree):
        suppressionLine = (
            node.lineno
            if location == 'definition'
            else _getDocstringEndLine(node)
        )
        if suppressionLine is None:
            continue

        codes = codesByLine.get(suppressionLine)
        if not codes:
            continue

        definitionLineToCodes.setdefault(node.lineno, set()).update(codes)

    return definitionLineToCodes


def _iterDocstringOwners(tree: ast.AST) -> Iterable[ClassOrFunctionDef]:
    """Yield all AST nodes that can own docstrings."""
    for node in ast.walk(tree):
        if isinstance(
            node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
        ):
            yield node


def _getDocstringEndLine(node: ast.AST) -> int | None:
    """Return the line number where the docstring ends, if present."""
    body = getattr(node, 'body', [])
    if not body:
        return None

    firstStmt = body[0]
    if not isinstance(firstStmt, ast.Expr):
        return None

    value = firstStmt.value

    if isinstance(value, ast.Constant) and isinstance(value.value, str):
        return getattr(firstStmt, 'end_lineno', firstStmt.lineno)

    if hasattr(value, 's') and isinstance(value.s, str):
        return getattr(firstStmt, 'end_lineno', firstStmt.lineno)

    return None

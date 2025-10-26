from __future__ import annotations

import ast
import re
import sys


def replaceTupleBracket(string: str) -> str:
    """
    Remove the comma in strings like "tuple[*Shape,]"

    We need to do this for Python 3.11 or newer, because when we write type
    annotations such as "tuple[*Shape]", the ast.unparse() returns
    "tuple[*Shape,]" (one more comma).

    For example, ``ast.unparse(ast.parse("tuple[*Shape]"))`` would return
    ``tuple[*Shape,]`` in Python 3.11+.

    For Python 3.10, ``tuple[*Shape]`` isn't a valid syntax, so we don't need
    to do this replacement.
    """
    return re.sub(r'(tuple|Tuple)\[\*(.*?),\]', r'\1[*\2]', string)


if sys.version_info >= (3, 11):

    def py311unparse(astObj: ast.AST) -> str:
        """Unparse an AST tree"""
        return replaceTupleBracket(ast.unparse(astObj))

    unparse = py311unparse
else:  # Python 3.10 only, because this project doesn't support Python 3.9
    unparse = ast.unparse


def unparseName(
        node: ast.expr | ast.Module | None,
) -> str | None:
    """Parse type annotations from argument list or return annotation."""
    if node is None:
        return None

    return unparse(node).strip()
